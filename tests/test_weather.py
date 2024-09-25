import pytest
from fastapi.testclient import TestClient
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis
import boto3
from botocore.exceptions import ClientError
from app.s3_client import get_s3_client
from app.settings import LOCALSTACK_ENDPOINT, S3_BUCKET_NAME, DYNAMODB_TABLE_NAME, AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME
from app.main import app  # Adjust the import based on your app structure

def setup_s3_bucket():
    s3 = boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )

    try:
        s3.head_bucket(Bucket=S3_BUCKET_NAME)
    except ClientError:
        s3.create_bucket(Bucket=S3_BUCKET_NAME)

def setup_dynamodb_table():
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )

    table_schema = {
        "TableName": DYNAMODB_TABLE_NAME,
        "KeySchema": [{"AttributeName": "city", "KeyType": "HASH"}],
        "AttributeDefinitions": [{"AttributeName": "city", "AttributeType": "S"}],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }

    try:
        dynamodb.describe_table(TableName=DYNAMODB_TABLE_NAME)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            dynamodb.create_table(**table_schema)
        else:
            raise

@pytest.fixture(scope="module")
def test_client():
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
    
    setup_s3_bucket()
    setup_dynamodb_table()
    
    with TestClient(app) as client:
        yield client

def test_get_weather_success(test_client):
    response = test_client.get("/weather/London/")
    assert response.status_code == 200

def test_get_weather_failure(test_client):
    response = test_client.get("/weather/InvalidCity/")
    assert response.status_code == 404