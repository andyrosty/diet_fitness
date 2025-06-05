# Database Migrations Guide

This guide explains how to run database migrations for the Diet Fitness project.

## Prerequisites

1. Make sure your database is running. If using Docker, start it with:
   ```bash
   docker-compose up -d
   ```

2. Ensure your `.env` file contains the correct database connection string:
   ```
   DATABASE_URL=postgresql://andyrosty:pass1234@localhost:5432/diet_fitness_db
   ```

## Running Migrations

### Generate a Migration

To generate a new migration after making changes to your models:

```bash
alembic revision --autogenerate -m "Description of changes"
```

This will create a new migration file in the `migrations/versions/` directory.

### Apply Migrations

To apply all pending migrations:

```bash
alembic upgrade head
```

### Other Useful Commands

- To apply migrations up to a specific version:
  ```bash
  alembic upgrade <revision_id>
  ```

- To downgrade to a previous version:
  ```bash
  alembic downgrade <revision_id>
  ```

- To downgrade one version:
  ```bash
  alembic downgrade -1
  ```

- To see the current migration version:
  ```bash
  alembic current
  ```

- To see migration history:
  ```bash
  alembic history
  ```

## Troubleshooting

If you encounter issues with migrations:

1. **Database connection issues**: 
   - Make sure your database is running
   - Verify the DATABASE_URL in your .env file
   - Test the connection with the provided script:
     ```bash
     python test_db_connection.py
     ```

2. **Missing environment variables**:
   - Ensure your .env file is in the project root
   - Make sure it contains the DATABASE_URL variable

3. **Model import issues**:
   - If you add new models, make sure they inherit from the Base class
   - If you create models in new files, import them in migrations/env.py

## Changes Made to Fix Migration Issues

The following changes were made to fix the migration issues:

1. Updated `migrations/env.py` to:
   - Explicitly import all models to ensure they're included in Base.metadata
   - Add error handling for missing DATABASE_URL

2. Updated `app/db/database.py` to:
   - Load environment variables with load_dotenv()
   - Add error handling for missing DATABASE_URL

These changes ensure that:
- Environment variables are properly loaded
- All models are included in migrations
- Clear error messages are provided if something is missing