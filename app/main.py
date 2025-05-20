"""
main.py: Entry point for the Fitness And Diet FastAPI application.
Loads environment variables, initializes the FastAPI app, and includes API routes.
"""
from fastapi import FastAPI
from dotenv import load_dotenv
from app.diet_fit_app.controller import router #Links to the controller

load_dotenv()  # Load environment variables from .env file

import os
# Retrieve API keys for external AI providers
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize FastAPI application
app = FastAPI(title="Fitness And Diet App")

# Mount API routes defined in the controller
app.include_router(router)
