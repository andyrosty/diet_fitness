# Testing

This directory contains unit tests for the Fitness And Diet App.

## Running Tests

1. Install test dependencies (if not already installed):
   ```
   pip install pytest
   ```
2. Run tests using pytest:
   ```
   pytest testing
   ```

## Test Files

- **conftest.py**: Pytest fixtures for the FastAPI app.
- **test_main.py**: Tests for app import and OpenAPI schema.
- **test_controller.py**: Tests for the `/fitness-plan` endpoint behavior.