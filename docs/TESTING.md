# Testing Guide for Fitness And Diet App

This document provides instructions for running tests and adding new tests to the Fitness And Diet App.

## Overview

The Fitness And Diet App includes several test scripts to verify different aspects of the application:

1. **Basic Application Import Test**: Verifies that the FastAPI application can be imported correctly
2. **Authentication Flow Test**: Tests the complete authentication flow (signup, login, protected endpoints)
3. **Database Connection Test**: Verifies that the application can connect to the database

## Prerequisites

Before running tests, ensure you have:

1. Installed all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up the environment variables in a `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/diet_fitness_db
   ```

3. Started the application and database:
   - If using Docker: `docker-compose up -d`
   - If running locally: `uvicorn app.main:app --reload`

## Running Tests

### Basic Application Import Test

This test verifies that the FastAPI application can be imported correctly:

```bash
python tests/test_app.py
```

Expected output:
```
Successfully imported the FastAPI app!
App routes: [...]
```

### Authentication Flow Test

This test verifies the complete authentication flow:

```bash
python tests/test_auth.py
```

This script will:
1. Create a test user account
2. Log in with the test user's credentials
3. Access a protected endpoint with the JWT token
4. Delete the test user account

### Database Connection Test

This test verifies that the application can connect to the database:

```bash
python tests/test_db_connection.py
```

Expected output on success:
```
Attempting to connect to database with URL: postgresql://username:password@localhost:5432/diet_fitness_db
SUCCESS: Connected to the database successfully!
```

## Running All Tests

To run all tests at once, you can use pytest:

```bash
pytest
```

## Adding New Tests

### Unit Tests

To add new unit tests:

1. Create a new test file in the `tests` directory with a name starting with `test_`
2. Import the necessary modules and functions
3. Write test functions with names starting with `test_`
4. Use assertions to verify expected behavior

Example:

```python
# tests/test_example.py
from app.some_module import some_function

def test_some_function():
    result = some_function(input_data)
    assert result == expected_output
```

### Integration Tests

For integration tests that require the application to be running:

1. Create a new test file in the `tests` directory
2. Use the `requests` library to make HTTP requests to the running application
3. Verify the responses match expected behavior

Example:

```python
# tests/test_integration_example.py
import requests

BASE_URL = "http://localhost:8000"

def test_some_endpoint():
    response = requests.get(f"{BASE_URL}/some-endpoint")
    assert response.status_code == 200
    assert "expected_data" in response.json()
```

### Test Coverage

To check test coverage:

1. Install the coverage package:
   ```bash
   pip install coverage
   ```

2. Run tests with coverage:
   ```bash
   coverage run -m pytest
   ```

3. Generate a coverage report:
   ```bash
   coverage report
   ```

4. For a more detailed HTML report:
   ```bash
   coverage html
   ```
   Then open `htmlcov/index.html` in your browser.

## Mocking External Services

When testing code that interacts with external services like OpenAI:

1. Use the `unittest.mock` module to mock external API calls
2. Create mock responses that mimic the expected API responses
3. Test your code's behavior with these mock responses

Example:

```python
from unittest.mock import patch, MagicMock

@patch('app.diet_fit_app.service.gpt03_agent.run')
def test_fitness_pipeline_with_mock(mock_run):
    # Set up mock response
    mock_result = MagicMock()
    mock_result.output = expected_output
    mock_run.return_value = mock_result
    
    # Call the function that uses the external service
    result = run_fitness_pipeline(test_input)
    
    # Assert the function behaved as expected
    assert result == expected_output
```

## Continuous Integration

The project is set up for continuous integration testing. When you submit a pull request:

1. All tests will automatically run
2. The pull request will show whether tests passed or failed
3. Code coverage reports will be generated

## Troubleshooting Tests

If tests are failing:

1. **Database connection issues**:
   - Ensure the database is running
   - Verify the DATABASE_URL in your .env file
   - Run `python tests/test_db_connection.py` to test the connection

2. **Application not running**:
   - For tests that require the application to be running, ensure it's started
   - Check the application logs for errors

3. **Authentication issues**:
   - Ensure the JWT_SECRET_KEY is set in your .env file
   - Check that the test user credentials are correct

4. **OpenAI API issues**:
   - Verify your OPENAI_API_KEY is valid
   - Consider mocking the OpenAI API calls for testing