"""
Database configuration module for the Diet Fitness application.

This module sets up the SQLAlchemy ORM connection to the database and provides
the necessary components for database operations throughout the application.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows database configuration to be stored securely outside of code
load_dotenv()

# Get database connection string from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set or is empty")

# Create SQLAlchemy engine for connecting to the database
# The engine is the starting point for any SQLAlchemy application
engine = create_engine(DATABASE_URL)

# Create a session factory bound to our engine
# Sessions are used for all database operations and transaction management
SessionLocal = sessionmaker(
    autocommit=False,  # Transactions won't be auto-committed
    autoflush=False,   # Changes won't be automatically flushed to the database
    bind=engine        # Connect sessions to our database engine
)

# Create a base class for declarative class definitions
# All ORM model classes will inherit from this base
Base = declarative_base()

def get_db():
    """
    FastAPI dependency for database session management.

    Creates a new SQLAlchemy session for each request and ensures
    proper cleanup when the request is complete.

    Yields:
        Session: SQLAlchemy database session

    Note:
        This function is designed to be used with FastAPI's dependency injection system.
        It automatically closes the session when the request is complete, even if an
        exception occurs during request processing.
    """
    # Create a new session for this request
    db = SessionLocal()
    try:
        # Provide the session to the route handler
        yield db
    finally:
        # Ensure the session is closed when the request is complete
        # This happens even if an exception is raised
        db.close()
