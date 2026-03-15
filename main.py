# Import FastAPI framework for building the API
from fastapi import FastAPI

# Import os module to read environment variables
import os

# Import requests library to fetch data from external APIs
import requests

# Import load_dotenv to load variables from the .env file
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Create the FastAPI application instance
app = FastAPI()

# Read the APP_ENV variable from the environment
APP_ENV = os.getenv("APP_ENV")


# Create a health check endpoint
@app.get("/health")
def health():
    # Return a JSON response that confirms the server is running
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": APP_ENV
    }


# Create an endpoint to analyze market trends using GitHub data
@app.get("/market-trends")
def market_trends():

    # Define the GitHub API URL for a popular repository
    url = "https://api.github.com/repos/openai/openai-python"

    # Send a GET request to the GitHub API
    response = requests.get(url)

    # Check if the API request was successful
    if response.status_code == 200:

        # Convert the API response into JSON format
        data = response.json()

        # Extract important data fields from the JSON
        repo_name = data["name"]
        stars = data["stargazers_count"]
        forks = data["forks_count"]

        # Create a simple trend score calculation
        trend_score = stars + forks

        # Return a customized JSON response
        return {
            "repository": repo_name,
            "stars": stars,
            "forks": forks,
            "trend_score": trend_score,
            "analysis": "This repository shows strong developer interest and market trend."
        }

    else:
        # Return a friendly error message if the API request fails
        return {
            "error": "External API is not available at the moment"
        }