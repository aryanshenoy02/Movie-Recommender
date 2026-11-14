# 🎌 Anime Recommendation System

A personalized anime recommendation system that suggests anime based on user ratings and preferences. The project combines machine learning, a REST API, a relational database, and a frontend interface to provide an interactive recommendation experience.

## 🚀 Overview

This project aims to provide personalized anime recommendations rather than relying solely on popularity or generic rankings.

Users can interact with the application, provide ratings, and receive recommendations based on their preferences.

The application is divided into three main components:

- **Machine Learning:** Processes anime data and generates personalized recommendations.
- **Backend API:** Handles user interactions, database operations, and communication between the frontend and ML model.
- **Frontend:** Provides the interface through which users interact with the recommendation system.

## 🧠 Machine Learning

The recommendation logic is implemented in `recomender.py`.

The ML component is responsible for processing anime information and generating recommendations based on user preferences and ratings.

Key aspects include:

- Processing anime-related data.
- Incorporating user ratings into the recommendation process.
- Using machine learning techniques to identify relevant anime.
- Generating personalized recommendations.
- Considering anime types to improve recommendation diversity and reduce repetitive suggestions.

The recommendation engine is integrated into the backend, allowing the API to retrieve recommendations when requested.

## ⚙️ Backend Architecture

The backend is implemented using **FastAPI**, with `main.py` serving as the central entry point.

Its responsibilities include:

- Exposing REST API endpoints.
- Handling incoming frontend requests.
- Managing user-related operations.
- Interacting with the SQLite database through SQLAlchemy.
- Connecting the recommendation engine with the application.
- Returning recommendation results to the frontend.

### Database

The project uses SQLite for persistent data storage, with SQLAlchemy handling database interactions.

The database is stored in `UserBase.db`.

It is used to maintain user-related information and ratings required by the application.

## 🖥️ Frontend

The frontend provides the user interface and communicates with the FastAPI backend.

It consists of:

- `index.html` – Main application structure.
- `style.css` – Styling and visual layout.
- `app.js` – Frontend JavaScript logic and API communication.

The frontend allows users to interact with the recommendation system without directly interacting with the underlying ML implementation.

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| Language | Python, JavaScript |
| Machine Learning | Scikit-learn, NumPy, Pandas |
| Backend | FastAPI |
| Database | SQLite |
| ORM | SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| API | REST API |

## 📁 Project Structure

```text
Anime-Recommendation-System/
│
├── main.py              # FastAPI backend and API endpoints
├── recomender.py        # Machine learning and recommendation logic
├── UserBase.db          # SQLite database
├── requirements.txt     # Python dependencies
│
├── index.html           # Frontend structure
├── style.css            # Frontend styling
├── app.js               # Frontend logic and API requests
│
└── README.md
```

## 💻 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/aryanshenoy02/Anime-Recommender.git
cd REPOSITORY-NAME
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Linux / macOS**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the backend

```bash
uvicorn main:app --reload
```

The FastAPI server should now be available at:

`http://127.0.0.1:8000`

FastAPI's interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

### 5. Launch the frontend

Open `index.html` in your browser if your frontend is configured to run independently.

Ensure the frontend API configuration points to the running backend.

## 🎯 Project Objectives

- Build a personalized recommendation system using machine learning.
- Integrate an ML model into a functional backend application.
- Develop REST API endpoints using FastAPI.
- Implement persistent storage using SQLite and SQLAlchemy.
- Connect a frontend application to an ML-powered backend.
- Explore the practical application of recommendation systems.

## 🔮 Future Improvements

- Improve recommendation quality through experimentation with different recommendation algorithms.
- Introduce more sophisticated user preference modelling.
- Improve recommendation diversity.
- Expand the dataset and anime metadata.
- Deploy the application for public access.
- Improve the frontend user experience.

## 👨‍💻 Author

**Aryan Shenoy**

GitHub: [@aryanshenoy02](https://github.com/aryanshenoy02)

---

*Built as a practical exploration of machine learning, recommendation systems, backend development, and full-stack application integration.*
