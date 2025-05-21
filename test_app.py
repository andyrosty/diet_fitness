import sys
import os

# Add the current directory to the Python path
sys.path.append(os.getcwd())

try:
    from app.main import app
    print("Successfully imported the FastAPI app!")
    print("App routes:", app.routes)
except Exception as e:
    print("Error importing the app:", e)