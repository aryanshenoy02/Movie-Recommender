import kagglehub
import pandas as pd
import difflib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
import numpy as np

import os
path = kagglehub.dataset_download("hamzaashfaque1999/myanimelist-scraped-data")

anime = pd.read_csv(os.path.join(path, 'anime_entries.csv'))
manga = pd.read_csv(os.path.join(path, 'manga_entries.csv'))


#CLEANING THE DATASET
anime = anime.drop(columns = ['japanese_name','german_name','english_name','french_name','spanish_name','airing_date','premier_date','broadcast_date','background'])

def clean_data(col:pd.Series):
    col = col.str.replace('[','')
    col = col.str.replace(']','')
    col = col.str.replace('"','')
    col = col.str.replace(' ','_')
    col = col.str.replace(',_',' ')
    col = col.fillna('')
    return col
anime['genres'] = clean_data(anime['genres'])
anime['studios'] = clean_data(anime['studios'])
anime['demographic'] = clean_data(anime['demographic'])
anime['description'] = anime['description'].fillna('')
anime['description'] = anime['description'].str.replace('No synopsis information has been added to this title. Help improve our database by adding a synopsis here .','')

def clean_themes(col:pd.Series):
    col = col.str.replace('[','')
    col = col.str.replace(']','')
    col = col.str.replace('"','')
    col = col.str.replace(',',' ')
    col = col.str.replace('  ',' ')

    col = col.fillna('')
    return col
anime['themes'] = clean_themes(anime['themes'])


#CREATING THE FEATURE MATRIX
tfid = TfidfVectorizer(stop_words = 'english')
ohe = OneHotEncoder()

genre_matrix = tfid.fit_transform(anime['genres'])
theme_matrix = tfid.fit_transform(anime['themes'])
studio_matrix = tfid.fit_transform(anime['studios'])
desc_matrix = tfid.fit_transform(anime['description'])
demo_matrix = ohe.fit_transform(anime[['demographic']])
type_matrix = ohe.fit_transform(anime[['item_type']])

#assigning weights:
genre_matrix*=0.4
theme_matrix*=0.4
studio_matrix*=0.1
desc_matrix*=0.2

matrix = hstack([genre_matrix, theme_matrix, studio_matrix, desc_matrix, demo_matrix,type_matrix ])



#CREATING NEAREST NEIGHBORS OBJECT
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_distances
recomender_knn = NearestNeighbors(
    n_neighbors = 20,
    metric = 'cosine'
)
recomender_knn.fit(matrix)

knn_fallback = NearestNeighbors(
    n_neighbors = 20,
    metric = 'cosine'
)
knn_fallback.fit(matrix)

#FINDING DISTANCE BETWEEN 2 ANIME
def BG_distance(idx1, idx2):
    #idx1 = recomendation
    #idx2 = seen
    distance = cosine_distances(
        matrix[idx1],
        matrix[idx2]
    )
    return distance[0][0]


#PERSONALIZING THE GRAPH DEPENDING ON USER RATINGS
#ratings_dict : {anime_name: user_rating}

def get_anime_idx(anime_name):
    matches = anime[anime['title_name'].str.lower() == anime_name.lower()]
    if len(matches) > 0:
        return matches.index[0]
        
    title_list = anime['title_name'].tolist()
    close_matches = difflib.get_close_matches(anime_name, title_list, n=1, cutoff=0.5)
    if close_matches:
        return anime[anime['title_name'] == close_matches[0]].index[0]
        
    contains_matches = anime[anime['title_name'].str.lower().str.contains(anime_name.lower(), na=False, regex=False)]
    if len(contains_matches) > 0:
        return contains_matches.index[0]
        
    raise ValueError(f"Anime '{anime_name}' not found")

def personalize_graph(ratings_dict):
    unranked_recommendations = {}

    for anime_name, user_rating in ratings_dict.items():

        #idx of anime_name in ratings_dict from the anime dataset
        try:
            idx = get_anime_idx(anime_name)
        except ValueError:
            continue
        
        #distance and index of each anime from the ratings_dict anime_name
        distances, indices = recomender_knn.kneighbors(
        matrix[idx], #distances
        n_neighbors = 30 #indices
        )

        #index and distances of each anime in the dataset to the target anime from the ratings_dict
        candidatedistances = distances[0][1:]
        candidateindices = indices[0][1:]

        filtered_candidates = []
        filtered_distances = []
        rated_titles = {title.lower() for title in ratings_dict}

        for candidate_idx, distance in zip(candidateindices, candidatedistances):
            candidate_title = anime.iloc[candidate_idx]['title_name'].lower()

            if candidate_title not in rated_titles:
                filtered_candidates.append(candidate_idx)
                filtered_distances.append(distance)

        candidateindices = filtered_candidates
        candidatedistances = filtered_distances
        
        for i, candidate_idx in enumerate(candidateindices):
            distance = BG_distance(candidate_idx, idx)
            if distance < 0.6:
                if user_rating >= 8:
                    candidatedistances[i] *= 0.25
                elif user_rating >= 6:
                    candidatedistances[i] *= 0.5
                else:
                    candidatedistances[i] *= 1.5
        #unranked_recommendations = {anime_name:{index(from dataset) of similar anime : distances from anime_name in ratings_dict}}
        unranked_recommendations[anime_name] = dict(zip(candidateindices, candidatedistances))

    
    for anime_name in unranked_recommendations:
        unranked_recommendations[anime_name] = dict(sorted(unranked_recommendations[anime_name].items(), key=lambda item: item[1]))
    
    return unranked_recommendations
    '''
    {
    "Naruto": {
        42: 0.03,
        17: 0.08,
        91: 0.20},

    "Bleach": {
        33: 0.30,
        17: 0.40,
        72: 0.60}
    }
    '''
#ACTUAL RECOMENDATION SYSTEM
#anime_name : target anime
#ratings_dict : {anime_name: user_rating}
def recomend(anime_name, ratings_dict):
    personalized_distances = personalize_graph(ratings_dict)
    idx = get_anime_idx(anime_name)
    list1 = []
    list2 = {}
    #make a list of 5-10 rated anime with minimum distance from target 
    for anime1, dic in personalized_distances.items():
        try:
            idx1 = get_anime_idx(anime1)
        except ValueError:
            continue
        #have to change this later to sort based on distance and then take the top 5-10
        if BG_distance(idx, idx1) < 0.4:
            list1.append(anime1)
    
    #contains all rated (watched) anime
    list1 = list1[0:5]
    #make a list2 of 20 unrated anime based on distance from rated anime in list1
    if len(list1) == 5:
        for anime_name in list1:
            for candidate_idx, distance in personalized_distances[anime_name].items():
                list2[candidate_idx] = distance
        sorted_list2 = dict(sorted(list2.items(), key=lambda item: item[1]))
        top_5_indices = list(sorted_list2.keys())[:5]
        top_5_anime = anime.iloc[top_5_indices]["title_name"].tolist()
        return top_5_anime

    else:
        fallback_distances, fallback_indices = knn_fallback.kneighbors(
            matrix[idx],
            n_neighbors=20
        )

        fallback_indices = fallback_indices[0][1:]  # remove target anime itself
        fallback_distances = fallback_distances[0][1:]

        # remove anime already rated by the user
        fallback_recommendations = []
        rated_titles = {title.lower() for title in ratings_dict}
        
        for candidate_idx, distance in zip(fallback_indices, fallback_distances):
            candidate_title = anime.iloc[candidate_idx]["title_name"].lower()

            if candidate_title not in rated_titles:
                fallback_recommendations.append(candidate_idx)

            if len(fallback_recommendations) == 5:
                break

        return anime.iloc[fallback_recommendations]["title_name"].tolist()


        
'''
so user puts in movie A that hes already seen. now the model spits out movie B C D E F in the same order of distances.
so B is most similar to A and so on. now if B is near a movie G which the user rated low then I'll have to put down B's
rank. now if G is close to B then it also must be close to A. (I have to make sure that the model doesnt give out seen anime.
so I have to make a col for that. lets assume that that feature is already there, I'll have to make it separately for the db
anyways). now I have to find out that B is near G. I have G's score already in ['userscore']. now if distance between
B and G < 0.6, and G has good rating then decrease distance between B and G and vice-versa. so now i have to find
distance between each recomendation and the ones in liking to compare.
'''

'''
candidatedistances = distances[0][1:]
    candidateindices = indices[0][1:]

    for i, candidate_idx in enumerate(candidateindices):
        for j in anime[anime['userscore'].notna()].index:
          distance = BG_distance(candidate_idx,j)
          if distance < 0.6:
                elif anime.loc[j, 'userscore'] == 'love':
                    candidatedistances[i] *= 0.25
                elif anime.loc[j, 'userscore'] == 'like':
                    candidatedistances[i] *= 0.5
                elif anime.loc[j, 'userscore'] == 'dislike':
                    candidatedistances[i] *= 1.5

    ranking = candidatedistances.argsort()
    recommended_indices = candidateindices[ranking]
    recommendations = anime.iloc[recommended_indices]['title_name']
    return recommendations.tolist()
'''

'''
unranked_recommendations = {
            candidate_idx: distance for candidate_idx, distance in zip(candidateindices, candidatedistances)
            }
    
'''

'''
#index of target anime
    #target_idx = get_anime_idx(anime_name)
    recomendations = personalize_graph(ratings_dict)

    rankings = recomendations[anime_name] 

    for index, dist in rankings.items():
        if anime.iloc[index]['title_name'] in ratings_dict.keys():
            del rankings[index]

    return rankings[:5]
'''