# Deployment Guide for Fitness And Diet App

This document provides instructions for deploying the Fitness And Diet App to various production environments.

## Prerequisites

Before deploying, ensure you have:

1. A production-ready version of the application
2. Access to a PostgreSQL database
3. An OpenAI API key
4. A server or cloud platform to host the application

## Environment Configuration

Create a `.env` file with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://username:password@hostname:5432/diet_fitness_db
JWT_SECRET_KEY=your_secure_jwt_secret_key
```

For production, ensure:
- Use a strong, randomly generated JWT_SECRET_KEY
- Store sensitive environment variables securely according to your hosting platform's recommendations
- Consider using a database connection pooling service for better performance

## Deployment Options

### Option 1: Docker Deployment

#### Prerequisites
- Docker and Docker Compose installed on the server
- Git access to clone the repository

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/diet_fitness.git
   cd diet_fitness
   ```

2. Create a `.env` file with your production environment variables

3. Build and start the containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. Run database migrations:
   ```bash
   docker-compose exec app alembic upgrade head
   ```

5. Set up a reverse proxy (like Nginx) to handle HTTPS and forward requests to the application

### Option 2: Cloud Platform Deployment

#### AWS Elastic Beanstalk

1. Install the AWS CLI and EB CLI:
   ```bash
   pip install awscli awsebcli
   ```

2. Initialize your EB application:
   ```bash
   eb init -p docker
   ```

3. Create an environment:
   ```bash
   eb create production-environment
   ```

4. Set environment variables:
   ```bash
   eb setenv OPENAI_API_KEY=your_openai_api_key DATABASE_URL=your_database_url JWT_SECRET_KEY=your_jwt_secret
   ```

5. Deploy the application:
   ```bash
   eb deploy
   ```

#### Heroku

1. Install the Heroku CLI:
   ```bash
   npm install -g heroku
   ```

2. Login to Heroku:
   ```bash
   heroku login
   ```

3. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

4. Add PostgreSQL add-on:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

5. Set environment variables:
   ```bash
   heroku config:set OPENAI_API_KEY=your_openai_api_key JWT_SECRET_KEY=your_jwt_secret
   ```

6. Deploy the application:
   ```bash
   git push heroku main
   ```

7. Run migrations:
   ```bash
   heroku run alembic upgrade head
   ```

### Option 3: Manual Deployment

#### Prerequisites
- Python 3.10 or higher installed on the server
- PostgreSQL database
- Nginx or another web server for reverse proxy

#### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/diet_fitness.git
   cd diet_fitness
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your production environment variables

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Set up a systemd service to run the application:
   ```
   [Unit]
   Description=Diet Fitness App
   After=network.target

   [Service]
   User=your_user
   WorkingDirectory=/path/to/diet_fitness
   Environment="PATH=/path/to/diet_fitness/venv/bin"
   EnvironmentFile=/path/to/diet_fitness/.env
   ExecStart=/path/to/diet_fitness/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

7. Enable and start the service:
   ```bash
   sudo systemctl enable diet_fitness
   sudo systemctl start diet_fitness
   ```

8. Set up Nginx as a reverse proxy:
   ```
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

9. Set up SSL with Let's Encrypt:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

## Production Considerations

### Security

1. **HTTPS**: Always use HTTPS in production
2. **JWT Secret**: Use a strong, randomly generated JWT secret key
3. **Database Credentials**: Use strong passwords and consider using IAM authentication where available
4. **API Keys**: Rotate API keys regularly and use environment variables
5. **Rate Limiting**: Implement rate limiting to prevent abuse

### Performance

1. **Database Indexing**: Ensure proper indexes are created for frequently queried fields
2. **Connection Pooling**: Use connection pooling for database connections
3. **Caching**: Implement caching for frequently accessed data
4. **Asynchronous Processing**: Use background workers for long-running tasks

### Monitoring

1. **Logging**: Set up comprehensive logging
2. **Error Tracking**: Use a service like Sentry for error tracking
3. **Performance Monitoring**: Monitor application performance with tools like New Relic or Datadog
4. **Alerting**: Set up alerts for critical errors or performance issues

### Scaling

1. **Horizontal Scaling**: Deploy multiple instances behind a load balancer
2. **Database Scaling**: Consider read replicas for database scaling
3. **Containerization**: Use Docker for consistent deployments across environments
4. **Orchestration**: Consider Kubernetes for container orchestration in large deployments

## Backup and Disaster Recovery

1. **Database Backups**: Set up regular database backups
2. **Backup Testing**: Regularly test restoring from backups
3. **Disaster Recovery Plan**: Document steps for recovery in case of failure

## Continuous Deployment

1. **CI/CD Pipeline**: Set up a CI/CD pipeline for automated testing and deployment
2. **Blue-Green Deployment**: Consider blue-green deployment for zero-downtime updates
3. **Rollback Plan**: Have a plan for rolling back deployments if issues are detected

## Maintenance

1. **Updates**: Regularly update dependencies and the application itself
2. **Security Patches**: Apply security patches promptly
3. **Database Maintenance**: Perform regular database maintenance
4. **Monitoring Review**: Regularly review monitoring data for potential issues