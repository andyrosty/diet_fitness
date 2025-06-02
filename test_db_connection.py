import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("ERROR: DATABASE_URL environment variable is not set or is empty")
    exit(1)

print(f"Attempting to connect to database with URL: {database_url}")

try:
    # Create engine and connect
    engine = create_engine(database_url)
    connection = engine.connect()
    print("SUCCESS: Connected to the database successfully!")
    connection.close()
except Exception as e:
    print(f"ERROR: Failed to connect to the database: {str(e)}")
    print("Make sure the database is running and the connection details are correct.")
    print("If using Docker, ensure the container is running with: docker-compose up -d")