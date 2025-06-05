# Authentication Implementation for Fitness And Diet App

This document describes the implementation of user authentication and database integration for the Fitness And Diet App.

## Features Implemented

1. **Database Setup**
   - PostgreSQL database integration with SQLAlchemy ORM
   - Models for users and fitness plans

2. **Authentication**
   - User signup and login with JWT tokens
   - Password hashing with bcrypt
   - Protected API endpoints

3. **Plan Storage**
   - Storage of generated fitness and diet plans
   - Retrieval of user-specific plans

## Setup Instructions

1. **Environment Variables**
   Make sure your `.env` file contains the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_URL=postgresql://username:password@localhost/diet_fitness_db
   JWT_SECRET_KEY=your_secret_key_here
   ```
   Replace the placeholder values with your actual credentials.

2. **Database Setup**
   - Install PostgreSQL if not already installed
   - Create a new database named `diet_fitness_db`
   - Update the `DATABASE_URL` in the `.env` file with your PostgreSQL credentials

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication
- `POST /auth/signup`: Create a new user account
  ```json
  {
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password"
  }
  ```

- `POST /auth/login`: Log in and get a JWT token
  ```
  username=your_username&password=your_password
  ```
  (Form data, not JSON)

### Protected Endpoints
- `POST /api/fitness-plan`: Generate and store a fitness plan
- `GET /api/my-plans`: Retrieve all fitness plans for the current user

## Testing

You can test the authentication functionality using the provided `test_auth.py` script:

```
python test_auth.py
```

This script will:
1. Create a test user
2. Log in with the test user's credentials
3. Access a protected endpoint with the JWT token

Note: The application must be running on localhost:8000 for the test to work.