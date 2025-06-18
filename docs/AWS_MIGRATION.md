# Migrating Your Diet Fitness App to AWS

This document provides a comprehensive plan to move your application to AWS, set up continuous deployment from GitHub, and ensure your iOS app can access the API.

## Current Setup

Your application currently uses:
- PostgreSQL 15 running in a Docker container
- Python 3.10 FastAPI application in a Docker container
- Docker Compose for local development and testing

## 1. Database Migration to AWS RDS

Your application currently uses PostgreSQL in a Docker container, which can be easily migrated to AWS RDS (Relational Database Service) using the AWS free tier:

### Step 1: Create an RDS PostgreSQL Instance

1. Log in to the AWS Management Console and navigate to RDS
2. Click "Create database"
3. Select PostgreSQL as the engine
4. Choose appropriate settings:
   - **For AWS Free Tier**: Select "Free tier" template
   - Instance type: db.t3.micro (included in free tier)
   - Storage: 20GB (free tier allows up to 20GB)
   - Disable storage autoscaling for free tier
   - Single-AZ deployment (Multi-AZ is not included in free tier)
5. Configure security settings:
   - Create a new VPC security group
   - Set a strong master password
6. Configure database options:
   - Name your database `diet_fitness_db`
   - Set initial database name, port (5432)
7. Create the database

### Step 2: Configure Security Group

1. Edit the RDS security group to allow connections:
   - From your application servers
   - From your development environment (temporarily for migration)

### Step 3: Migrate Your Data

For a one-time migration:

```bash
# Export data from your local database
pg_dump -h localhost -U andyrosty -d diet_fitness_db > diet_fitness_backup.sql

# Import data to RDS
psql -h your-rds-endpoint.amazonaws.com -U master_username -d diet_fitness_db < diet_fitness_backup.sql
```

### Step 4: Update Application Configuration

Update your `.env` file with the new RDS connection string:

```
DATABASE_URL=postgresql://master_username:master_password@your-rds-endpoint.amazonaws.com:5432/diet_fitness_db
```

## 2. Deploying the Application to AWS

You have several options for hosting your FastAPI application on AWS, with considerations for the AWS free tier:

### Option A: AWS Elastic Beanstalk (Recommended for Simplicity and Free Tier)

Elastic Beanstalk is included in the AWS Free Tier, which provides:
- 750 hours of t2.micro instance usage per month
- 5GB of S3 storage for application versions

1. Install the EB CLI:
   ```bash
   pip install awsebcli
   ```

2. Initialize your EB application:
   ```bash
   eb init -p docker
   ```

3. Create an environment with free tier settings:
   ```bash
   eb create production-environment --instance-type t2.micro --single
   ```

4. Set environment variables:
   ```bash
   eb setenv OPENAI_API_KEY=your_openai_api_key DATABASE_URL=your_rds_url JWT_SECRET_KEY=your_jwt_secret
   ```

5. Deploy the application:
   ```bash
   eb deploy
   ```

### Option B: AWS ECS (Elastic Container Service) with Fargate

This option provides more control and scalability, but has limited free tier options:

**Free Tier Considerations:**
- ECR: First 500MB of storage per month is free for 12 months
- ECS with EC2 launch type: Can use t2.micro instances under free tier
- Fargate: Not included in free tier, but provides serverless container management

Steps:
1. Create an ECR repository for your Docker image
   ```bash
   aws ecr create-repository --repository-name diet-fitness-app
   ```

2. Set up an ECS cluster (with EC2 launch type for free tier)
   ```bash
   aws ecs create-cluster --cluster-name diet-fitness-cluster
   ```

3. Define a task definition and service using t2.micro instances if using EC2 launch type
4. Configure environment variables in the task definition
5. Set up an Application Load Balancer (note: ALB has limited free tier offerings)

## 3. Migrating from Docker to AWS

Since your application is already containerized with Docker, the migration to AWS is simplified. Here's how to transition from your current Docker setup to AWS:

### Docker Compose to AWS Migration

1. **Database Migration**:
   - Your current PostgreSQL container (postgres:15) will be replaced by RDS
   - Update your application's DATABASE_URL environment variable to point to the RDS instance
   - Perform data migration as described in Section 1

2. **Application Container**:
   - Your current application container can be deployed directly to Elastic Beanstalk or ECS
   - The existing Dockerfile can be used without modifications
   - Docker Compose won't be needed in production as AWS services will manage the infrastructure

3. **Environment Variables**:
   - Transfer all environment variables from docker-compose.yml to your AWS environment
   - For Elastic Beanstalk, use `eb setenv` as shown earlier
   - For ECS, define environment variables in the task definition

4. **Local Development**:
   - Continue using Docker Compose for local development
   - Create separate configuration for development and production environments

## 4. Setting Up Continuous Deployment from GitHub

### Using GitHub Actions (Current Implementation)

The project currently uses GitHub Actions for CI/CD, which automatically builds, tests, and deploys the application to AWS Elastic Beanstalk when changes are pushed to the main branch.

1. The workflow is defined in `.github/workflows/ci-cd.yml`
2. It runs on push to main branch and on pull requests
3. The workflow consists of two main jobs:
   - `build-and-test`: Builds the application and runs tests
   - `deploy`: Deploys the application to AWS (only on main branch)

### CI/CD Workflow Steps

1. **Build and Test**:
   - Checkout code
   - Set up Python environment
   - Install dependencies
   - Run tests locally
   - Build Docker image
   - Run tests inside Docker

2. **Deploy to AWS**:
   - Configure AWS credentials
   - Login to Amazon ECR
   - Build, tag, and push Docker image to ECR
   - Install AWS Elastic Beanstalk CLI
   - Update Dockerrun.aws.json with correct ECR repository and image tag
   - Deploy to Elastic Beanstalk

### Sample GitHub Actions Workflow

```yaml
name: AWS CI/CD Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests locally
        run: pytest

      - name: Build Docker image
        run: docker build -t diet-fitness-app:latest .

      - name: Run tests inside Docker
        run: docker run --rm diet-fitness-app:latest pytest

  deploy:
    needs: build-and-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build, tag, and push image to Amazon ECR
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: diet-fitness-app
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest

      - name: Install AWS EB CLI
        run: |
          pip install awsebcli

      - name: Update Dockerrun.aws.json
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: diet-fitness-app
          AWS_REGION: ${{ secrets.AWS_REGION }}
        run: |
          # Replace placeholders in Dockerrun.aws.json
          sed -i "s|ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com|$ECR_REGISTRY|g" Dockerrun.aws.json
          sed -i "s|diet-fitness-app:latest|$ECR_REPOSITORY:${{ github.sha }}|g" Dockerrun.aws.json

      - name: Deploy to Elastic Beanstalk
        env:
          EB_APP_NAME: diet-fitness-app
          EB_ENV_NAME: production-environment
        run: |
          eb init $EB_APP_NAME --platform docker --region ${{ secrets.AWS_REGION }}
          eb deploy $EB_ENV_NAME --version ${{ github.sha }}
```

## 5. Making the API Accessible from an iOS App

### API Gateway Configuration

1. Set up an API Gateway to provide a consistent endpoint for your iOS app
2. Configure CORS to allow requests from your iOS app
3. Set up proper authentication using JWT tokens
4. Consider implementing API keys for additional security

### iOS App Integration

1. Use HTTPS for all API calls
2. Implement proper error handling for network requests
3. Store the API endpoint in a configuration file
4. Implement token-based authentication in your iOS app
5. Consider using a library like Alamofire for API requests

### Sample Swift Code for API Integration

```swift
import Alamofire

struct APIClient {
    static let baseURL = "https://your-api-gateway-url.amazonaws.com/api"
    static var authToken: String?

    static func login(username: String, password: String, completion: @escaping (Result<String, Error>) -> Void) {
        let parameters: [String: String] = [
            "username": username,
            "password": password
        ]

        AF.request("\(baseURL)/auth/login", 
                   method: .post, 
                   parameters: parameters, 
                   encoder: JSONParameterEncoder.default)
            .responseDecodable(of: LoginResponse.self) { response in
                switch response.result {
                case .success(let loginResponse):
                    authToken = loginResponse.access_token
                    completion(.success(loginResponse.access_token))
                case .failure(let error):
                    completion(.failure(error))
                }
            }
    }

    static func getFitnessPlans(completion: @escaping (Result<[FitnessPlan], Error>) -> Void) {
        guard let token = authToken else {
            completion(.failure(APIError.notAuthenticated))
            return
        }

        let headers: HTTPHeaders = [
            "Authorization": "Bearer \(token)"
        ]

        AF.request("\(baseURL)/api/my-plans", 
                   method: .get, 
                   headers: headers)
            .responseDecodable(of: [FitnessPlan].self) { response in
                switch response.result {
                case .success(let plans):
                    completion(.success(plans))
                case .failure(let error):
                    completion(.failure(error))
                }
            }
    }
}
```

## 6. Security Considerations

1. **Secrets Management**:
   - Use AWS Secrets Manager to store database credentials, API keys, and JWT secrets
   - Update your application to retrieve secrets at runtime

2. **Network Security**:
   - Place your RDS instance in a private subnet
   - Use security groups to restrict access
   - Consider using a VPC endpoint for AWS services

3. **API Security**:
   - Implement rate limiting
   - Use AWS WAF to protect against common web exploits
   - Ensure proper validation of all inputs

## 7. Monitoring and Logging

**Free Tier Considerations:**
- CloudWatch: Free tier includes 10 custom metrics, 10 alarms, and 1 million API requests per month
- Basic monitoring for EC2, EBS, and RDS is included at no additional cost

1. Set up CloudWatch for monitoring:
   - Application logs
   - RDS metrics
   - API Gateway metrics
   - Limit custom metrics to stay within free tier limits

2. Configure alarms for:
   - High database CPU/memory usage
   - API errors
   - Application errors
   - Prioritize critical alarms to stay within the 10-alarm free tier limit

## Next Steps

1. **Plan Free Tier Usage**: Determine which AWS services to use within free tier limits
2. **Create AWS Infrastructure**: Start by setting up your RDS instance and application hosting environment using free tier options
3. **Migrate Docker Setup**: Follow the migration steps in Section 3 to move from Docker to AWS
4. **Update Application Configuration**: Modify your code to work with AWS services
5. **Set Up CI/CD Pipeline**: Configure GitHub Actions workflow for CI/CD (already implemented in `.github/workflows/ci-cd.yml`)
6. **Test Thoroughly**: Verify all functionality works in the AWS environment
7. **Monitor Costs**: Set up AWS Budgets to monitor and alert on costs to avoid exceeding free tier limits
8. **Update iOS App**: Configure your iOS app to use the new API endpoints
