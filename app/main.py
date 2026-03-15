# Import FastAPI framework
from fastapi import FastAPI

# Import requests library to call external APIs
import requests

# Import os module to read environment variables
import os

# Import database session and base
from app.database import SessionLocal, engine

# Import database models
from app.models import Base, Idea

# Import Pydantic schema for request validation
from app.schemas import IdeaCreate


# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)


# Create FastAPI application with metadata
app = FastAPI(
    title="StartSmart API",
    description="Backend API that helps entrepreneurs analyze market trends before launching a business.",
    version="1.0.0"
)


# Root endpoint for API information
@app.get("/")
def read_root():
    # Return basic information about the API
    return {
        "message": "Welcome to StartSmart API",
        "description": "API that helps entrepreneurs analyze market trends before starting a business",
        "version": "1.0.0"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    # This endpoint is used to verify that the API is running correctly
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


# Endpoint to fetch market trends from an external API
@app.get("/market-trends")
def get_market_trends():

    # Example external API (GitHub public API)
    url = "https://api.github.com/search/repositories?q=startup&sort=stars&order=desc"

    # Send GET request to external API
    response = requests.get(url)

    # Check if request was successful
    if response.status_code != 200:
        return {
            "error": "External API is unavailable"
        }

    # Parse JSON response
    data = response.json()

    # Extract useful data from response
    items = data["items"][:3]

    # Create simplified result list
    trends = []

    for repo in items:
        trends.append({
            "name": repo["name"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"]
        })

    # Return processed trend data
    return {
        "market_trends": trends
    }


# Endpoint to create a new idea in the database
@app.post("/ideas")
def create_idea(idea: IdeaCreate):

    # Create database session
    db = SessionLocal()

    # Create Idea object using request data
    new_idea = Idea(
        idea=idea.idea,
        description=idea.description
    )

    # Add idea to database session
    db.add(new_idea)

    # Commit transaction to save idea
    db.commit()

    # Refresh object to get updated values (like id)
    db.refresh(new_idea)

    # Close database session
    db.close()

    # Return created idea
    return new_idea


# Endpoint to retrieve all saved ideas
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