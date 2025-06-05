# Docker Usage Guide for Diet Fitness Application

This document explains how to use Docker to build and run the Diet Fitness application. For initial setup instructions, please refer to [DOCKER_SETUP.md](DOCKER_SETUP.md).

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your system
- OpenAI API key (if you're using OpenAI features)

## Environment Variables

Before running the application, you need to set up environment variables:

1. Create a `.env` file in the root directory of the project:

```
OPENAI_API_KEY=your_openai_api_key_here
```

The database connection is already configured in the docker-compose.yml file, so you don't need to specify it in the .env file.

## Building and Running

To build and run the application:

```bash
# Build and start the containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the containers
docker-compose down
```

The application will be available at http://localhost:8000

## Development Workflow

The Docker setup includes a volume mount that maps your local code to the container. This means:

1. You can make changes to the code on your local machine
2. The changes will be reflected in the container
3. With the reload option enabled in uvicorn, the application will automatically restart when code changes are detected

## Database Migrations

If you need to run database migrations:

```bash
# Access the application container
docker-compose exec app bash

# Run migrations
alembic upgrade head
```

## Troubleshooting

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Ensure all environment variables are correctly set
3. Try rebuilding the containers: `docker-compose up -d --build`
