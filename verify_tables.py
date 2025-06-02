import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("ERROR: DATABASE_URL environment variable is not set or is empty")
    exit(1)

print(f"Connecting to database with URL: {database_url}")

try:
    # Create engine and connect
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    # Get all table names
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")
    
    # Check for specific tables
    expected_tables = ['users', 'user_plans', 'workout_plans', 'diet_plans', 'alembic_version']
    missing_tables = [table for table in expected_tables if table not in tables]
    
    if missing_tables:
        print(f"WARNING: The following expected tables are missing: {missing_tables}")
    else:
        print("SUCCESS: All expected tables are present in the database!")
    
    # Print details of each table
    for table in tables:
        print(f"\nTable: {table}")
        print("Columns:")
        for column in inspector.get_columns(table):
            print(f"  - {column['name']} ({column['type']})")
        
        print("Indexes:")
        for index in inspector.get_indexes(table):
            print(f"  - {index['name']} on {index['column_names']}")
        
        if inspector.get_foreign_keys(table):
            print("Foreign Keys:")
            for fk in inspector.get_foreign_keys(table):
                print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    
except Exception as e:
    print(f"ERROR: Failed to inspect the database: {str(e)}")