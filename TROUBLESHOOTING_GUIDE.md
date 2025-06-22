# Troubleshooting Guide for Diet Fitness App

This guide will help you resolve common issues when setting up and running the Diet Fitness App.

## Environment Setup

### 1. Environment Variables

The application requires several environment variables to be set correctly in the `.env` file:

```
# Database connection string
DATABASE_URL=postgresql://andyrosty:pass1234@localhost:5432/diet_fitness_db

# OpenAI API key for AI features
OPENAI_API_KEY=your_openai_api_key_here

# JWT secret key for authentication
JWT_SECRET_KEY=your_secure_jwt_secret_key_here
```

Make sure to:
- Replace `your_openai_api_key_here` with your actual OpenAI API key
- Replace `your_secure_jwt_secret_key_here` with a secure random string for JWT token signing

### 2. Python Environment

1. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### 3. Database Setup

#### Option 1: Local PostgreSQL

If you want to run PostgreSQL locally:

1. Install PostgreSQL on your system
2. Create a database named `diet_fitness_db`
3. Create a user `andyrosty` with password `pass1234`
4. Grant all privileges on `diet_fitness_db` to `andyrosty`

Example PostgreSQL commands:
```sql
CREATE DATABASE diet_fitness_db;
CREATE USER andyrosty WITH PASSWORD 'pass1234';
GRANT ALL PRIVILEGES ON DATABASE diet_fitness_db TO andyrosty;
```

#### Option 2: Docker PostgreSQL

If you prefer to use Docker for just the database:
```
docker run --name diet_fitness_db -e POSTGRES_USER=andyrosty -e POSTGRES_PASSWORD=pass1234 -e POSTGRES_DB=diet_fitness_db -p 5432:5432 -d postgres:15
```

## Running the Application

### Option 1: Run with Python

After setting up the environment and database:
```
uvicorn app.main:app --reload
```

### Option 2: Run with Docker Compose

This is the recommended approach as it sets up both the application and database:

1. Make sure Docker and Docker Compose are installed
2. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY=your_openai_api_key_here
   ```
3. Run the application with Docker Compose:
   ```
   docker-compose up
   ```

## Running Tests

### Basic Tests

Run basic tests with SQLite:
```
pytest
```

### PostgreSQL Tests

To run tests with PostgreSQL:
```
RUN_PG_TESTS=1 pytest
```

## Common Issues

### 1. "command not found" errors

If you encounter "command not found" errors for Python commands:
- Ensure Python is installed and in your PATH
- Activate your virtual environment

### 2. Database connection errors

If you encounter database connection errors:
- Verify PostgreSQL is running
- Check that the database, user, and password match your .env file
- Ensure the PostgreSQL port (5432) is not blocked by a firewall

#### Fallback SQLite Database

The application now includes a fallback to an in-memory SQLite database when PostgreSQL is not available. This allows the application to start and provide minimal functionality even when the main database is not accessible.

When using the fallback database:
- Data will not be persisted between application restarts
- Some features that require specific PostgreSQL functionality may not work
- You'll see warning messages in the console about the database connection

To disable this fallback and force the application to exit when the database is not available, set the environment variable:
```
FAIL_ON_DB_ERROR=1
```

### 3. OpenAI API errors

If you encounter OpenAI API errors:
- Verify your API key is correct
- Check that you have sufficient credits in your OpenAI account

### 4. JWT authentication errors

If you encounter JWT authentication errors:
- Ensure JWT_SECRET_KEY is set in your .env file
- Try logging out and logging in again

### 5. HTTP 503 Service Unavailable errors

If you receive a 503 Service Unavailable response from the API:
- This usually indicates that the database connection failed during the request
- Check that PostgreSQL is running and properly configured
- See the database connection errors section above for more troubleshooting steps

#### Common Database Connection Errors

If you see an error like "Textual SQL expression 'SELECT 1' should be explicitly declared as text('SELECT 1')" in the logs:
- This is related to SQLAlchemy's query execution
- The application has been updated to handle this properly
- If you're developing custom database queries, remember to use SQLAlchemy's text() function for raw SQL:
  ```python
  from sqlalchemy import text
  db.execute(text("YOUR SQL QUERY HERE"))
  ```
