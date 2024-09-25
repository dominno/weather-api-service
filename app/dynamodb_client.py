from aiobotocore.session import get_session

from app.settings import DYNAMODB_TABLE_NAME, LOCALSTACK_ENDPOINT, AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME

async def log_event_to_dynamodb(city: str, timestamp: str, s3_url: str):
    session = get_session()
    async with session.create_client(
        'dynamodb',
        endpoint_url=LOCALSTACK_ENDPOINT,  # LocalStack's endpoint
        aws_access_key_id=AWS_ACCESS_KEY,  # Dummy credentials
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    ) as dynamodb_client:
        item = {
            "city": {"S": city},
            "timestamp": {"S": timestamp},
            "s3_url": {"S": s3_url},
        }
        await dynamodb_client.put_item(TableName=DYNAMODB_TABLE_NAME, Item=item)
