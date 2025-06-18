"""
Database connection test script.

This script verifies that the application can connect to the database using
the test database session. It's a diagnostic tool to help troubleshoot database 
connectivity issues during testing.
"""
import pytest
from sqlalchemy.orm import Session

def test_db_connection(db):
    """Test that we can connect to the database"""
    # The db fixture from conftest.py provides a working database session
    assert db is not None
    assert isinstance(db, Session)

    # Test that we can execute a simple query
    result = db.execute("SELECT 1").scalar()
    assert result == 1
