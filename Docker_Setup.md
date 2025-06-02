
# Setting Up the Database with Docker for the Diet Fitness Project

Based on the project files, We will be using PostgreSQL with SQLAlchemy and Alembic for migrations. Here's a step-by-step guide to set up your database using Docker:

## 1. Create a docker-compose.yml file

First, create a `docker-compose.yml` file in the root of your project:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: diet_fitness_db
    environment:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: diet_fitness_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## 2. Start the PostgreSQL container

Run the following command to start the PostgreSQL container:

```bash
docker-compose up -d
```

This will download the PostgreSQL image if it's not already available and start the container in detached mode.

## 3. Update your .env file (if needed)

Your current `.env` file has the database URL set to:
```
DATABASE_URL=postgresql://username:password@localhost/diet_fitness_db
```

This should work as is since we're mapping the container's port 5432 to the host's port 5432. However, if you're running the application inside another Docker container, you'll need to update the URL to use the service name:

```
DATABASE_URL=postgresql://username:password@postgres/diet_fitness_db
```

## 4. Run database migrations

Now that your database is running, you need to run the migrations to create the tables. First, make sure Alembic is properly configured:

1. Update the `target_metadata` in `migrations/env.py`:

```python
# Add these imports at the top
from app.db.models import Base
from app.db.database import engine

# Update the target_metadata line
target_metadata = Base.metadata
```

2. Update the database URL in `alembic.ini` or ensure it's being read from the environment:

```python
# In migrations/env.py, add:
import os
from dotenv import load_dotenv

load_dotenv()

# Override sqlalchemy.url from alembic.ini
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
```

3. Run the migrations:

```bash
# Generate a migration
alembic revision --autogenerate -m "Initial migration"

# Apply the migration
alembic upgrade head
```

## 5. Verify the setup

You can verify that your database is properly set up by connecting to it:

```bash
docker exec -it diet_fitness_db psql -U username -d diet_fitness_db
```

Once connected, you can list the tables:

```sql
\dt
```

You should see the tables defined in your models: `users`, `user_plans`, `workout_plans`, and `diet_plans`.

## 6. Running your application

Now you can run your application, and it should connect to the PostgreSQL database running in Docker:

```bash
# Make sure your virtual environment is activated
python -m app.main
```

## Additional Tips

1. **Database Backups**: You can create backups of your database using:
   ```bash
   docker exec -t diet_fitness_db pg_dump -U username diet_fitness_db > backup.sql
   ```

2. **Restoring Backups**:
   ```bash
   cat backup.sql | docker exec -i diet_fitness_db psql -U username -d diet_fitness_db
   ```

3. **Accessing PostgreSQL logs**:
   ```bash
   docker logs diet_fitness_db
   ```

4. **Stopping the container**:
   ```bash
   docker-compose down
   ```

5. **Stopping and removing volumes** (caution: this will delete all data):
   ```bash
   docker-compose down -v
   ```

This setup provides a clean, isolated PostgreSQL instance for your Diet Fitness application that can be easily started, stopped, and reset as needed during development.