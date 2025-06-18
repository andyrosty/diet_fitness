"""
main.py: Entry point for the Fitness And Diet FastAPI application.
Loads environment variables, initializes the FastAPI app, and includes API routes.
"""
from fastapi import FastAPI
from dotenv import load_dotenv

from app.diet_fit_app.controller import router as diet_router
from app.auth.controller import router as auth_router
from app.db.database import engine
from app.db import models

# Load environment variables from .env file
load_dotenv()

# Retrieve API key for external AI provider
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Create database tables when running normally (skip during tests/import)
if os.getenv("TEST_MODE") != "1":
    models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(title="Fitness And Diet App")

# Mount API routes
app.include_router(auth_router, prefix="/auth")
app.include_router(diet_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
