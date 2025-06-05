"""
FastAPI application import test script.

This script verifies that the FastAPI application can be imported correctly,
which helps diagnose import errors, path issues, or other initialization problems.
It's a simple diagnostic tool to ensure the application is properly configured.
"""
import sys
import os

# Add the parent directory to the Python path
# This ensures the app package can be found regardless of how the script is run
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Attempt to import the FastAPI application
    from app.main import app
    print("Successfully imported the FastAPI app!")

    # Print the registered routes to verify the API structure
    print("App routes:", app.routes)
except Exception as e:
    # Provide detailed error information if import fails
    print("Error importing the app:", e)