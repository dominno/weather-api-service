# Project Documentation

## Overview

This project is a weather API service that fetches weather data from the OpenWeather API, caches the results in Redis, and logs events to DynamoDB. The service is containerized using Docker and can be deployed locally or to a production environment.

## Features

- Fetches weather data from the OpenWeather API.
- Caches weather data in Redis for faster subsequent requests.
- Logs weather data events to DynamoDB.
- Provides a FastAPI-based RESTful API.

## Prerequisites

- Docker
- Docker Compose
- Python 3.9

## Local Deployment

### Step 1: Clone the Repository

```sh
git clone <repository-url>
cd weather-api-service
```

### Step 2: Build and Run Docker Containers

```sh
docker-compose up --build
```

The API will be available at `http://localhost:8000/weather`.

### Step 3: Access API Documentation

The API documentation is available at `http://localhost:8000/docs` when running locally.

## Running Unit Tests

### Run Tests

The tests will automatically run as part of the Docker Compose setup.

```sh
python scripts/test_runner.py
```

## Production Deployment

### Step 1: Set Up AWS Credentials

Ensure your AWS credentials are configured in your environment. You can use the AWS CLI to configure them:

```sh
aws configure
```

### Step 2: Run the Deployment Script

Execute the `deploy_to_aws.py` script to automate the deployment process:

```sh
python scripts/deploy_to_aws.py
```

This script will:
- Create an ECR repository.
- Build and push the Docker image to ECR.
- Create an ECS cluster.
- Register an ECS task definition.
- Create and run an ECS service.## Production Deployment

### Step 1: Set Up AWS Credentials

Ensure your AWS credentials are configured in your environment. You can use the AWS CLI to configure them:

```sh
aws configure
```

### Step 2: Run the Deployment Script

Execute the `deploy_to_aws.py` script to automate the deployment process:

```sh
python scripts/deploy_to_aws.py
```

This script will:
- Create an ECR repository.
- Build and push the Docker image to ECR.
- Create an ECS cluster.
- Register an ECS task definition.
- Create and run an ECS service.
## Conclusion

This documentation provides a comprehensive guide to deploying, testing, and running the Weather API Service both locally and in a production environment. For more details, refer to the codebase and the provided code references.
