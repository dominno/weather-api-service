import boto3
import subprocess
import json

# AWS Configuration
AWS_REGION = 'your-region'
ECR_REPO_NAME = 'your-repo-name'
CLUSTER_NAME = 'your-cluster-name'
TASK_DEFINITION_NAME = 'your-task-def-name'
SERVICE_NAME = 'your-service-name'
CONTAINER_NAME = 'your-container-name'
IMAGE_TAG = 'latest'
KEY_PAIR_NAME = 'your-key-pair-name'
PEM_FILE_PATH = 'path/to/your-key-pair.pem'

# Create ECR repository
def create_ecr_repo():
    ecr = boto3.client('ecr', region_name=AWS_REGION)
    response = ecr.create_repository(repositoryName=ECR_REPO_NAME)
    repo_uri = response['repository']['repositoryUri']
    print(f"ECR repository '{ECR_REPO_NAME}' created with URI: {repo_uri}")
    return repo_uri

# Build and push Docker image to ECR
def build_and_push_docker_image(repo_uri):
    subprocess.run(['docker', 'build', '-t', f'{repo_uri}:{IMAGE_TAG}', '.'])
    subprocess.run(['docker', 'push', f'{repo_uri}:{IMAGE_TAG}'])
    print(f"Docker image pushed to ECR: {repo_uri}:{IMAGE_TAG}")

# Create ECS cluster
def create_ecs_cluster():
    ecs = boto3.client('ecs', region_name=AWS_REGION)
    ecs.create_cluster(clusterName=CLUSTER_NAME)
    print(f"ECS cluster '{CLUSTER_NAME}' created.")

# Register ECS task definition
def register_task_definition(repo_uri):
    ecs = boto3.client('ecs', region_name=AWS_REGION)
    response = ecs.register_task_definition(
        family=TASK_DEFINITION_NAME,
        networkMode='awsvpc',
        containerDefinitions=[
            {
                'name': CONTAINER_NAME,
                'image': f'{repo_uri}:{IMAGE_TAG}',
                'memory': 512,
                'cpu': 256,
                'essential': True,
                'portMappings': [
                    {
                        'containerPort': 80,
                        'hostPort': 80,
                        'protocol': 'tcp'
                    }
                ],
                'environment': [
                    {'name': 'S3_BUCKET_NAME', 'value': 'your-bucket-name'},
                    {'name': 'DYNAMODB_TABLE_NAME', 'value': 'your-table-name'},
                    {'name': 'AWS_ACCESS_KEY', 'value': 'your-access-key'},
                    {'name': 'AWS_SECRET_KEY', 'value': 'your-secret-key'},
                    {'name': 'REGION_NAME', 'value': 'your-region'}
                ]
            }
        ],
        requiresCompatibilities=['FARGATE'],
        cpu='256',
        memory='512',
        executionRoleArn='arn:aws:iam::your-account-id:role/ecsTaskExecutionRole',
        taskRoleArn='arn:aws:iam::your-account-id:role/ecsTaskExecutionRole'
    )
    print(f"Task definition '{TASK_DEFINITION_NAME}' registered.")
    return response['taskDefinition']['taskDefinitionArn']

# Create and run ECS service
def create_ecs_service(task_definition_arn):
    ecs = boto3.client('ecs', region_name=AWS_REGION)
    response = ecs.create_service(
        cluster=CLUSTER_NAME,
        serviceName=SERVICE_NAME,
        taskDefinition=task_definition_arn,
        desiredCount=1,
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ['your-subnet-id'],
                'securityGroups': ['your-security-group-id'],
                'assignPublicIp': 'ENABLED'
            }
        }
    )
    print(f"ECS service '{SERVICE_NAME}' created and running.")

if __name__ == "__main__":
    repo_uri = create_ecr_repo()
    build_and_push_docker_image(repo_uri)
    create_ecs_cluster()
    task_definition_arn = register_task_definition(repo_uri)
    create_ecs_service(task_definition_arn)