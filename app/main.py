# Import FastAPI framework for building the API
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

# Import Pydantic schema
from schemas import IdeaCreate

# Load environment variables from .env file
load_dotenv()

# Create database tables automatically
Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI()

# Read environment variable
APP_ENV = os.getenv("APP_ENV")


# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/health")
def health():
    # Return JSON response to confirm the API is running
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": APP_ENV
    }


# -----------------------------
# Market Trends Endpoint
# -----------------------------
@app.get("/market-trends")
def market_trends():

    # GitHub API URL for a popular repository
    url = "https://api.github.com/repos/openai/openai-python"

    # Send GET request to GitHub API
    response = requests.get(url)

    # Check if API request succeeded
    if response.status_code == 200:

        # Convert response to JSON
        data = response.json()

        # Extract important metrics
        repo_name = data["name"]
        stars = data["stargazers_count"]
        forks = data["forks_count"]

        # Simple trend score calculation
        trend_score = stars + forks

        # Return analyzed market trend data
        return {
            "repository": repo_name,
            "stars": stars,
            "forks": forks,
            "trend_score": trend_score,
            "analysis": "This repository shows strong developer interest and market trend."
        }

    else:
        # Return error message if external API fails
        return {
            "error": "External API is not available at the moment"
        }


# -----------------------------
# POST Endpoint to Save Ideas
# -----------------------------
@app.post("/ideas")
def create_idea(idea: IdeaCreate):

    # Create database session
    db = SessionLocal()

    # Create new Idea object
    new_idea = Idea(
        idea=idea.idea,
        description=idea.description
    )

    # Add object to database
    db.add(new_idea)

    # Commit transaction
    db.commit()

    # Close database session
    db.close()

    return {"message": "Idea saved successfully"}


# -----------------------------
# GET Endpoint to Retrieve Ideas
# -----------------------------
@app.get("/ideas")
def get_ideas():

    # Create database session
    db = SessionLocal()

    # Query all saved ideas
    ideas = db.query(Idea).all()

    # Close database session
    db.close()

    # Return list of ideas
    return ideas