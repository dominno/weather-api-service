import boto3
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.settings import LOCALSTACK_ENDPOINT, S3_BUCKET_NAME, DYNAMODB_TABLE_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME


def setup_s3_bucket():
    """Create an S3 bucket in LocalStack if it doesn't already exist."""
    s3 = boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )

    try:
        # Check if the bucket already exists
        s3.head_bucket(Bucket=S3_BUCKET_NAME)
        print(f"S3 bucket '{S3_BUCKET_NAME}' already exists.")
    except ClientError:
        # Bucket does not exist, so create it
        s3.create_bucket(Bucket=S3_BUCKET_NAME)
        print(f"S3 bucket '{S3_BUCKET_NAME}' created successfully.")


def setup_dynamodb_table():
    """Create a DynamoDB table in LocalStack if it doesn't already exist."""
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )

    # Define table schema
    table_schema = {
        "TableName": DYNAMODB_TABLE_NAME,
        "KeySchema": [{"AttributeName": "city", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "city", "AttributeType": "S"}],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }

    try:
        # Check if table already exists
        dynamodb.describe_table(TableName=DYNAMODB_TABLE_NAME)
        print(f"DynamoDB table '{DYNAMODB_TABLE_NAME}' already exists.")
    except ClientError as e:
        # Table does not exist, so create it
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            dynamodb.create_table(**table_schema)
            print(f"DynamoDB table '{DYNAMODB_TABLE_NAME}' created successfully.")
        else:
            raise


def verify_services():
    """Verify that S3 bucket and DynamoDB table are set up correctly."""
    # S3 Verification
    s3 = boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )

    try:
        response = s3.head_bucket(Bucket=S3_BUCKET_NAME)
        print(f"Verified: S3 bucket '{S3_BUCKET_NAME}' exists.")
    except ClientError as e:
        print(f"Failed to verify S3 bucket: {e}")

    # DynamoDB Verification
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )

    try:
        response = dynamodb.describe_table(TableName=DYNAMODB_TABLE_NAME)
        print(f"Verified: DynamoDB table '{DYNAMODB_TABLE_NAME}' exists.")
    except ClientError as e:
        print(f"Failed to verify DynamoDB table: {e}")


if __name__ == "__main__":
    logger.info("setup_localstack.py script is running")
    
    # Setup S3 and DynamoDB in LocalStack
    setup_s3_bucket()
    setup_dynamodb_table()

    # Verify the services are set up correctly
    print("\nVerifying LocalStack services...")
    verify_services()
