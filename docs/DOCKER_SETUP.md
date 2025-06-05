
# Docker Setup for the Diet Fitness Project

This guide explains how to set up Docker for the Diet Fitness project, which includes both a FastAPI application and a PostgreSQL database. For usage instructions after setup, please refer to [DOCKER_USAGE.md](DOCKER_USAGE.md).

## 1. Project Docker Structure

The project uses Docker Compose to manage two containers:
1. A FastAPI application container
2. A PostgreSQL database container

## 2. Create a Dockerfile

First, create a `Dockerfile` in the root of your project:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 3. Create a docker-compose.yml file

Next, create a `docker-compose.yml` file in the root of your project:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: diet_fitness_app
    environment:
      DATABASE_URL: postgresql://andyrosty:pass1234@postgres:5432/diet_fitness_db
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    restart: unless-stopped
    volumes:
      - ./:/app

  postgres:
    image: postgres:15
    container_name: diet_fitness_db
    environment:
      POSTGRES_USER: andyrosty
      POSTGRES_PASSWORD: pass1234
      POSTGRES_DB: diet_fitness_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## 4. Create a .env file

Create a `.env` file in the root directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 5. Start the containers

Run the following command to build and start both containers:

```bash
docker-compose up -d
```

This will:
1. Build the application image using the Dockerfile
2. Download the PostgreSQL image if it's not already available
3. Start both containers in detached mode

## 6. Run database migrations

Now that your database is running, you need to run the migrations to create the tables. The project already has Alembic configured, so you can run the migrations directly:

```bash
# Access the application container
docker-compose exec app bash

# Run migrations
alembic upgrade head
```

Alternatively, you can run the migrations from your host machine if you have alembic installed:

```bash
# Make sure your virtual environment is activated and dependencies installed
alembic upgrade head
```

## 7. Verify the database setup

You can verify that your database is properly set up by connecting to it:

```bash
docker exec -it diet_fitness_db psql -U andyrosty -d diet_fitness_db
```

Once connected, you can list the tables:

```sql
\dt
```

You should see the tables defined in your models.

## 8. Running your application

The application should now be running and accessible at http://localhost:8000. You can verify this by opening the URL in your browser or using curl:

```bash
curl http://localhost:8000/docs
```

This will access the Swagger documentation for your API.

## Additional Tips

1. **Database Backups**: You can create backups of your database using:
   ```bash
   docker exec -t diet_fitness_db pg_dump -U andyrosty -d diet_fitness_db > backup.sql
   ```

2. **Restoring Backups**:
   ```bash
   cat backup.sql | docker exec -i diet_fitness_db psql -U andyrosty -d diet_fitness_db
   ```

3. **Accessing PostgreSQL logs**:
   ```bash
   docker logs diet_fitness_db
   ```

4. **Accessing Application logs**:
   ```bash
   docker logs diet_fitness_app
   ```

5. **Stopping the containers**:
   ```bash
   docker-compose down
   ```

6. **Stopping and removing volumes** (caution: this will delete all data):
   ```bash
   docker-compose down -v
   ```

7. **Rebuilding the application container** (after code changes):
   ```bash
   docker-compose up -d --build
   ```

This setup provides a complete Docker environment for your Diet Fitness application that includes both the application and database containers, making it easy to develop, test, and deploy.
