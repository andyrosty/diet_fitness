# Troubleshooting Guide for Fitness And Diet App

This document provides solutions to common issues that you might encounter when setting up, running, or using the Fitness And Diet App.

## Installation Issues

### Docker Installation

#### Issue: Docker containers fail to start

**Symptoms:**
- `docker-compose up -d` command fails
- Containers start but exit immediately

**Solutions:**
1. Check if the ports are already in use:
   ```bash
   sudo lsof -i :8000
   sudo lsof -i :5432
   ```
   If they are, stop the services using those ports or change the ports in docker-compose.yml.

2. Check Docker logs:
   ```bash
   docker-compose logs
   ```

3. Ensure your .env file exists and contains the required variables:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

#### Issue: Database container starts but application can't connect

**Symptoms:**
- PostgreSQL container is running
- Application container fails with database connection errors

**Solutions:**
1. Ensure the database URL in docker-compose.yml matches the PostgreSQL container configuration:
   ```
   DATABASE_URL: postgresql://andyrosty:pass1234@postgres:5432/diet_fitness_db
   ```
   Note that the hostname should be `postgres` (the service name), not `localhost`.

2. Check if the database is initialized:
   ```bash
   docker-compose exec postgres psql -U andyrosty -d diet_fitness_db -c "\dt"
   ```

3. Run migrations manually:
   ```bash
   docker-compose exec app alembic upgrade head
   ```

### Manual Installation

#### Issue: Dependencies installation fails

**Symptoms:**
- `pip install -r requirements.txt` command fails

**Solutions:**
1. Ensure you're using Python 3.10 or higher:
   ```bash
   python --version
   ```

2. Update pip:
   ```bash
   pip install --upgrade pip
   ```

3. Install dependencies one by one to identify the problematic package:
   ```bash
   pip install package-name
   ```

#### Issue: Application fails to start

**Symptoms:**
- `uvicorn app.main:app --reload` command fails

**Solutions:**
1. Check if all environment variables are set:
   ```bash
   cat .env
   ```

2. Ensure the database is running and accessible:
   ```bash
   python tests/test_db_connection.py
   ```

3. Check for syntax errors in your code:
   ```bash
   python -m py_compile app/main.py
   ```

## Database Issues

### Issue: Migrations fail

**Symptoms:**
- `alembic upgrade head` command fails

**Solutions:**
1. Check if the database exists and is accessible:
   ```bash
   python tests/test_db_connection.py
   ```

2. Check alembic version:
   ```bash
   alembic current
   ```

3. Reset migrations (caution: this will delete all data):
   ```bash
   # Drop all tables
   docker-compose exec postgres psql -U andyrosty -d diet_fitness_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
   
   # Recreate migrations
   alembic revision --autogenerate -m "reset migrations"
   alembic upgrade head
   ```

### Issue: Database connection errors

**Symptoms:**
- Application logs show database connection errors

**Solutions:**
1. Verify database credentials in .env file:
   ```
   DATABASE_URL=postgresql://username:password@hostname:5432/diet_fitness_db
   ```

2. Check if PostgreSQL is running:
   ```bash
   # For Docker
   docker ps | grep postgres
   
   # For local installation
   sudo systemctl status postgresql
   ```

3. Check PostgreSQL logs:
   ```bash
   # For Docker
   docker-compose logs postgres
   
   # For local installation
   sudo journalctl -u postgresql
   ```

## API Issues

### Issue: Authentication fails

**Symptoms:**
- Login endpoint returns 401 Unauthorized
- Protected endpoints return 401 Unauthorized even with token

**Solutions:**
1. Ensure you're using the correct username and password for login

2. Check if the JWT token is properly formatted in the Authorization header:
   ```
   Authorization: Bearer your_token_here
   ```

3. Verify the JWT_SECRET_KEY is set correctly in the .env file

4. Check token expiration (default is 30 minutes)

### Issue: API requests timeout

**Symptoms:**
- Requests to the fitness-plan endpoint timeout

**Solutions:**
1. Check OpenAI API key validity:
   ```bash
   curl -X POST https://api.openai.com/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -d '{
       "model": "gpt-3.5-turbo",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```

2. Increase the timeout settings in your client application

3. Check application logs for errors:
   ```bash
   # For Docker
   docker-compose logs app
   
   # For local installation
   tail -f app.log
   ```

## AI Integration Issues

### Issue: OpenAI API errors

**Symptoms:**
- Fitness plan generation fails with OpenAI API errors

**Solutions:**
1. Verify your OpenAI API key is valid and has sufficient credits

2. Check for rate limiting issues:
   ```
   Error: 429 - Rate limit exceeded
   ```
   If you see this error, wait a few minutes before trying again or upgrade your OpenAI plan.

3. Check for model availability issues:
   ```
   Error: 404 - Model not found
   ```
   If you see this error, ensure you're using a valid model name (e.g., "gpt-3.5-turbo" or "gpt-4o").

### Issue: Generated plans are incomplete or incorrect

**Symptoms:**
- Workout or diet plans are missing days
- Plans don't match user preferences

**Solutions:**
1. Check the user input data for completeness and clarity

2. Verify the system prompts in service.py are correctly formatted

3. Try using a more capable model (e.g., upgrade from GPT-3.5 to GPT-4o)

## Performance Issues

### Issue: Application is slow

**Symptoms:**
- API requests take a long time to complete
- UI feels sluggish

**Solutions:**
1. Check database query performance:
   ```bash
   # For Docker
   docker-compose exec postgres psql -U andyrosty -d diet_fitness_db -c "EXPLAIN ANALYZE SELECT * FROM user_plans WHERE user_id = 1;"
   ```

2. Add database indexes for frequently queried fields:
   ```sql
   CREATE INDEX idx_user_plans_user_id ON user_plans(user_id);
   ```

3. Implement caching for frequently accessed data

4. Use asynchronous processing for long-running tasks

## Common Error Messages and Solutions

### "Error: OPENAI_API_KEY environment variable is not set or is empty"

**Solution:**
Add your OpenAI API key to the .env file:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### "Error: DATABASE_URL environment variable is not set or is empty"

**Solution:**
Add your database URL to the .env file:
```
DATABASE_URL=postgresql://username:password@hostname:5432/diet_fitness_db
```

### "Error: JWT_SECRET_KEY environment variable is not set or is empty"

**Solution:**
Add a JWT secret key to the .env file:
```
JWT_SECRET_KEY=your_secure_jwt_secret_key
```

### "Error: Username already registered"

**Solution:**
Use a different username when registering a new account.

### "Error: Email already registered"

**Solution:**
Use a different email address when registering a new account.

### "Error: Incorrect username or password"

**Solution:**
Double-check your username and password. If you've forgotten your password, there's currently no password reset functionality. You'll need to create a new account.

## Getting Help

If you've tried the solutions in this guide and are still experiencing issues:

1. Check the application logs for more detailed error messages
2. Search for similar issues in the project's GitHub repository
3. Open a new issue on GitHub with:
   - A detailed description of the problem
   - Steps to reproduce the issue
   - Error messages and logs
   - Your environment details (OS, Docker version, etc.)