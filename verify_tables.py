"""
Database schema verification script.

This script connects to the database and inspects its structure to verify that:
1. All expected tables exist
2. Each table has the correct columns, indexes, and foreign keys

It's a diagnostic tool to help ensure the database schema is correctly set up
before running the application, especially after migrations or schema changes.
"""
import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows database configuration to be stored securely outside of code
load_dotenv()

# Get database connection string from environment variables
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("ERROR: DATABASE_URL environment variable is not set or is empty")
    exit(1)

print(f"Connecting to database with URL: {database_url}")

try:
    # Create SQLAlchemy engine and inspector for schema introspection
    engine = create_engine(database_url)
    inspector = inspect(engine)

    # Get all table names from the database
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")

    # Check for specific tables that should exist in the application
    expected_tables = ['users', 'user_plans', 'workout_plans', 'diet_plans', 'alembic_version']
    missing_tables = [table for table in expected_tables if table not in tables]

    # Report on missing tables if any
    if missing_tables:
        print(f"WARNING: The following expected tables are missing: {missing_tables}")
    else:
        print("SUCCESS: All expected tables are present in the database!")

    # Print detailed information about each table's structure
    for table in tables:
        print(f"\nTable: {table}")

        # List all columns and their data types
        print("Columns:")
        for column in inspector.get_columns(table):
            print(f"  - {column['name']} ({column['type']})")

        # List all indexes for performance optimization
        print("Indexes:")
        for index in inspector.get_indexes(table):
            print(f"  - {index['name']} on {index['column_names']}")

        # List all foreign keys for referential integrity
        if inspector.get_foreign_keys(table):
            print("Foreign Keys:")
            for fk in inspector.get_foreign_keys(table):
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

except Exception as e:
    # Provide helpful error information if inspection fails
    print(f"ERROR: Failed to inspect the database: {str(e)}")
