# Migrating Your Diet Fitness App to AWS

This document provides a comprehensive plan to move your application to AWS, set up continuous deployment from GitHub, and ensure your iOS app can access the API.

## 1. Database Migration to AWS RDS

Your application currently uses PostgreSQL, which can be easily migrated to AWS RDS (Relational Database Service):

### Step 1: Create an RDS PostgreSQL Instance

1. Log in to the AWS Management Console and navigate to RDS
2. Click "Create database"
3. Select PostgreSQL as the engine
4. Choose appropriate settings:
   - Dev/Test or Production tier based on your needs
   - Instance size (start with t3.micro for testing)
   - Storage (start with 20GB, enable auto-scaling)
   - Multi-AZ deployment for production environments
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

You have several options for hosting your FastAPI application on AWS:

### Option A: AWS Elastic Beanstalk (Recommended for Simplicity)

1. Install the EB CLI:
   ```bash
   pip install awsebcli
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
   eb setenv OPENAI_API_KEY=your_openai_api_key DATABASE_URL=your_rds_url JWT_SECRET_KEY=your_jwt_secret
   ```

5. Deploy the application:
   ```bash
   eb deploy
   ```

### Option B: AWS ECS (Elastic Container Service) with Fargate

This option provides more control and scalability:

1. Create an ECR repository for your Docker image
2. Set up an ECS cluster with Fargate
3. Define a task definition and service
4. Configure environment variables in the task definition
5. Set up an Application Load Balancer

## 3. Setting Up Continuous Deployment from GitHub

### Using AWS CodePipeline with GitHub Source

1. Create a CodePipeline in the AWS Console
2. Configure the source stage to use GitHub (version 2)
3. Connect to your GitHub repository
4. Set up a build stage using AWS CodeBuild:
   - Use a buildspec.yml file to define build steps
   - Include steps to run tests
   - Build and push Docker image to ECR
5. Configure a deploy stage:
   - For Elastic Beanstalk: Use the EB deployment action
   - For ECS: Update the ECS service

### Sample buildspec.yml for CodeBuild

```yaml
version: 0.2

phases:
  pre_build:
    commands:
      - echo Logging in to Amazon ECR...
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
      - REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/diet-fitness-app
      - COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)
      - IMAGE_TAG=${COMMIT_HASH:=latest}
  build:
    commands:
      - echo Build started on `date`
      - echo Building the Docker image...
      - docker build -t $REPOSITORY_URI:latest .
      - docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG
  post_build:
    commands:
      - echo Build completed on `date`
      - echo Pushing the Docker images...
      - docker push $REPOSITORY_URI:latest
      - docker push $REPOSITORY_URI:$IMAGE_TAG
      - echo Writing image definitions file...
      - aws ecs describe-task-definition --task-definition diet-fitness-task --query taskDefinition > taskdef.json
      - envsubst < appspec_template.yaml > appspec.yaml

artifacts:
  files:
    - appspec.yaml
    - taskdef.json
```

## 4. Making the API Accessible from an iOS App

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

## 5. Security Considerations

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

## 6. Monitoring and Logging

1. Set up CloudWatch for monitoring:
   - Application logs
   - RDS metrics
   - API Gateway metrics

2. Configure alarms for:
   - High database CPU/memory usage
   - API errors
   - Application errors

## Next Steps

1. **Create AWS Infrastructure**: Start by setting up your RDS instance and application hosting environment
2. **Update Application Configuration**: Modify your code to work with AWS services
3. **Set Up CI/CD Pipeline**: Configure GitHub integration with AWS CodePipeline
4. **Test Thoroughly**: Verify all functionality works in the AWS environment
5. **Update iOS App**: Configure your iOS app to use the new API endpoints