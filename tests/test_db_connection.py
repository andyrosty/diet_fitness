"""
Database connection test script.

This script verifies that the application can connect to the database using
the connection string specified in the environment variables. It's a diagnostic
tool to help troubleshoot database connectivity issues before running the main
application.
"""
import os
import sys
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Add the parent directory to the Python path to ensure we can find the .env file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from .env file
# This allows database configuration to be stored securely outside of code
load_dotenv()

# Get database connection string from environment variables
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("ERROR: DATABASE_URL environment variable is not set or is empty")
    exit(1)

print(f"Attempting to connect to database with URL: {database_url}")

try:
    # Create SQLAlchemy engine and attempt to establish a connection
    engine = create_engine(database_url)
    connection = engine.connect()
    print("SUCCESS: Connected to the database successfully!")

    # Properly close the connection when done
    connection.close()
except Exception as e:
    # Provide helpful error information and troubleshooting tips
    print(f"ERROR: Failed to connect to the database: {str(e)}")
    print("Make sure the database is running and the connection details are correct.")
    print("If using Docker, ensure the container is running with: docker-compose up -d")