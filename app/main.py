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
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("\n\033[91mError connecting to database:\033[0m", str(e))
        print("\n\033[93mPlease make sure PostgreSQL is running and properly configured.\033[0m")
        print("\033[93mSee the Troubleshooting Guide (TROUBLESHOOTING_GUIDE.md) for more information.\033[0m\n")
        if os.getenv("FAIL_ON_DB_ERROR", "0") != "1":
            print("\033[93mContinuing without database connection...\033[0m\n")
        else:
            print("\033[93mExiting due to database connection error.\033[0m\n")
            exit(1)

# Initialize FastAPI application
app = FastAPI(title="Fitness And Diet App")

# Mount API routes
app.include_router(auth_router, prefix="/auth")
app.include_router(diet_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
