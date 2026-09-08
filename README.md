🎬 Anime Recommender

An end-to-end anime recommendation system that generates personalized recommendations based on user ratings.

The project integrates a recommendation pipeline, SQLite database, REST API, and frontend UI into a complete full-stack ML application.

 🚀 Features

* Personalized anime recommendations based on user ratings
* Recommendation engine built with Python and scikit-learn
* User and rating data stored in SQLite
* REST API for communicating between the frontend and recommendation system
* Web-based frontend for interacting with the recommender

 🧠 How It Works

The application follows this flow:

User
  ↓
Frontend
  ↓
API
  ↓
Recommendation Engine
  ↓
SQLite Database
  ↓
Personalized Recommendations


The recommendation engine processes anime information and user ratings to find anime that are similar to the user's preferences.

🛠️ Tech Stack

* **Python**
* **scikit-learn**
* **FastAPI**
* **SQLite**
* **HTML / CSS / JavaScript**

📁 Project Structure

text
anime-recommender/
│
├── main.py            # API / backend
├── recomender.py      # Recommendation pipeline
├── UserBase.db        # SQLite database
│
├── index.html         # Frontend
├── style.css          # Frontend styling
└── app.js             # Frontend logic


🎯 Purpose

This project was built as a hands-on way to learn how different parts of an ML application fit together.

Instead of building only a recommendation model, I wanted to understand how to connect:

ML → Database → API → Frontend

into one complete application.

📚 What I Learned

* Building a recommendation system with scikit-learn
* Working with similarity-based recommendations
* Connecting Python applications to SQLite
* Building API endpoints with FastAPI
* Connecting a frontend to a backend using HTTP requests
* Structuring an ML project as an end-to-end application

🔮 Future Improvements

* Improve recommendation quality
* Add user authentication
* Add more sophisticated recommendation algorithms
* Improve the UI/UX
* Deploy the application
* Add more anime metadata and user interaction signals
