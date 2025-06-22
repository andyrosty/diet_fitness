# Known Issues in Diet Fitness App

This document outlines known issues and challenges in the Diet Fitness App project, focusing particularly on requirements and testing phases.

## Environment Setup Issues

1. **Python Environment**: The Python environment is not properly set up. Running basic Python commands like `pip` results in "command not found" errors.

2. **Dependencies Installation**: Unable to install dependencies from requirements.txt due to the Python environment issue.

## Testing Issues

1. **Disabled Tests in CI/CD Pipeline**: Tests are commented out in the CI/CD pipeline (.github/workflows/ci-cd.yml), indicating there are issues with the tests that have led to them being temporarily disabled.

2. **Test Environment Variables**: Tests require environment variables that may not be properly set:
   - OPENAI_API_KEY: Required for AI functionality
   - DATABASE_URL: Required for database connections
   - JWT_SECRET_KEY: Required for authentication

3. **PostgreSQL Tests Configuration**: PostgreSQL tests are conditionally run based on environment variables (RUN_PG_TESTS or CI), which may lead to inconsistent test coverage.

4. **Test Documentation Discrepancy**: The TESTING.md document suggests running individual test files directly with Python (e.g., `python tests/test_app.py`), but the test files are designed to be run with pytest.

## Requirements Issues

1. **Environment Variables**: The .env file contains placeholders for critical environment variables (OPENAI_API_KEY, JWT_SECRET_KEY) that reference other environment variables rather than actual values.

2. **Dependency Versions**: Some dependencies in requirements.txt have specific version constraints that might cause compatibility issues:
   - fastapi>=0.110.0 (relatively recent version)
   - pydantic>=2.10.0 (relatively recent version)
   - pydantic-ai==0.2.9 (pinned to a specific version)

3. **Missing Implementation**: Based on TASKS.md, some features might be partially implemented or in progress:
   - User authentication
   - Database integration
   - Plan storage


## Next Steps

To address these issues:

1. Set up a proper Python virtual environment
2. Install all dependencies from requirements.txt
3. Configure all required environment variables
4. Run tests to identify specific test failures
5. Fix test failures
6. Re-enable tests in the CI/CD pipeline
7. Complete any missing implementations based on TASKS.md
8. Update documentation to reflect the current state of the project