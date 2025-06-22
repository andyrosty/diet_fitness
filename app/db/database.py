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
try:
    engine = create_engine(DATABASE_URL)

    # Create a session factory bound to our engine
    # Sessions are used for all database operations and transaction management
    SessionLocal = sessionmaker(
        autocommit=False,  # Transactions won't be auto-committed
        autoflush=False,   # Changes won't be automatically flushed to the database
        bind=engine        # Connect sessions to our database engine
    )
except Exception as e:
    import sys
    print(f"\n\033[91mError initializing database engine:\033[0m {str(e)}", file=sys.stderr)
    print("\033[93mSetting up a fallback engine for minimal functionality.\033[0m", file=sys.stderr)

    # Create a fallback in-memory SQLite engine for minimal functionality
    # This allows the application to start even if PostgreSQL is not available
    from sqlalchemy.pool import StaticPool
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

        If the database connection fails, it will log the error and raise an HTTPException
        with a 503 Service Unavailable status code.
    """
    # Create a new session for this request
    try:
        db = SessionLocal()
        try:
            # Test the connection by executing a simple query
            db.execute("SELECT 1")
            # Provide the session to the route handler
            yield db
        finally:
            # Ensure the session is closed when the request is complete
            # This happens even if an exception is raised
            db.close()
    except Exception as e:
        import sys
        from fastapi import HTTPException, status

        print(f"\n\033[91mDatabase connection error in request:\033[0m {str(e)}", file=sys.stderr)
        print("\033[93mSee the Troubleshooting Guide (TROUBLESHOOTING_GUIDE.md) for database setup instructions.\033[0m\n", file=sys.stderr)

        # Raise an HTTPException with a 503 Service Unavailable status code
        # This will be caught by FastAPI and returned as a proper HTTP response
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable. Please try again later."
        )
