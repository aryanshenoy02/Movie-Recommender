# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException, Depends

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

import recomender as p

app = FastAPI(title = "Giving Awesome Anime Recommendations")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine("sqlite:///./UserBase.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        #lets an api endpoint use the db session as a dependency, and automatically close it after the request is done
        yield db
    finally:
        db.close()

#sqlalchemy models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    anime_title = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)

# create database tables
Base.metadata.create_all(bind=engine)

#pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Rate(BaseModel):
    anime_title: str
    rating: int

#homepage
@app.get("/")
def read_root():
    return {"message": "Welcome to the Anime recom!!!"}

#create new user
@app.post("/register", response_model=UserResponse)
def register_user(user:UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username taken")
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#login existing user
@app.post("/login", response_model=UserResponse)
def login_user(user:UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if existing_user.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return existing_user

#get all ratings for a user
@app.get("/ratings/{user_id}", response_model=List[Rate])
def get_ratings(user_id: int, db: Session = Depends(get_db)):
    ratings = db.query(Ratings).filter(Ratings.user_id == user_id).all()
    return ratings

#add a new rating for a user
@app.post("/rate/{user_id}/{anime_title}", response_model = Rate)
def add_rating(rate: Rate, user_id: int, anime_title: str, db: Session = Depends(get_db)):
    new_rating = Ratings(user_id=user_id, anime_title=anime_title, rating=rate.rating)
    if db.query(Ratings).filter(Ratings.user_id == user_id, Ratings.anime_title == anime_title).first():
        raise HTTPException(status_code=400, detail="Update your rating")
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

#updating an existing rating for a user
@app.put("/rate/{user_id}/{anime_title}", response_model = Rate)
def update_rating(rate: Rate, user_id: int, anime_title: str, db: Session = Depends(get_db)):
    rating = db.query(Ratings).filter(Ratings.user_id == user_id, Ratings.anime_title == anime_title).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    rating.rating = rate.rating
    db.commit()
    db.refresh(rating)
    return rating

#get recommendations
@app.get("/recommendations/{user_id}/{anime_title}")
def get_recommendations(user_id: int, anime_title: str, db: Session = Depends(get_db)):
    ratings = db.query(Ratings).filter(Ratings.user_id == user_id).all()
    ratings_dict = {r.anime_title: r.rating for r in ratings}
    try:
        recommendations = p.recomend(anime_title, ratings_dict)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
