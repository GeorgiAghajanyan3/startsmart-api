# Import FastAPI framework to build the API
from fastapi import FastAPI

# Import os module to work with environment variables
import os

# Import requests library to fetch data from external APIs
import requests

# Import dotenv to load variables from .env file
from dotenv import load_dotenv

# Import database engine and session
from database import engine, SessionLocal

# Import database models
from models import Base, Idea

# Load environment variables
load_dotenv()

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI()

# Read environment variable
APP_ENV = os.getenv("APP_ENV")


# -----------------------------
# Health check endpoint
# -----------------------------
@app.get("/health")
def health():
    # Return JSON response to confirm server is running
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": APP_ENV
    }


# -----------------------------
# Market trends endpoint
# -----------------------------
@app.get("/market-trends")
def market_trends():

    # GitHub API URL
    url = "https://api.github.com/repos/openai/openai-python"

    # Send GET request to GitHub API
    response = requests.get(url)

    # Check if request succeeded
    if response.status_code == 200:

        # Convert response to JSON
        data = response.json()

        # Extract important information
        repo_name = data["name"]
        stars = data["stargazers_count"]
        forks = data["forks_count"]

        # Calculate a simple trend score
        trend_score = stars + forks

        # Return custom JSON response
        return {
            "repository": repo_name,
            "stars": stars,
            "forks": forks,
            "trend_score": trend_score,
            "analysis": "This repository shows strong developer interest and market trend."
        }

    else:
        # Return friendly error if API fails
        return {
            "error": "External API is not available at the moment"
        }


# -----------------------------
# POST endpoint to save ideas
# -----------------------------
@app.post("/ideas")
def create_idea(idea: str, description: str):

    # Create database session
    db = SessionLocal()

    # Create Idea object
    new_idea = Idea(idea=idea, description=description)

    # Add object to database
    db.add(new_idea)

    # Commit transaction
    db.commit()

    # Close session
    db.close()

    return {"message": "Idea saved successfully"}


# -----------------------------
# GET endpoint to retrieve ideas
# -----------------------------
@app.get("/ideas")
def get_ideas():

    # Create database session
    db = SessionLocal()

    # Query all ideas from database
    ideas = db.query(Idea).all()

    # Close session
    db.close()

    # Return list of ideas
    return ideas