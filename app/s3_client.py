import json

from app.settings import S3_BUCKET_NAME, LOCALSTACK_ENDPOINT, AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME
from aiobotocore.session import get_session

def get_s3_client():
    session = get_session()
    return session.create_client(
        's3',
        endpoint_url=LOCALSTACK_ENDPOINT,  # LocalStack's endpoint
        aws_access_key_id=AWS_ACCESS_KEY,  # Dummy credentials for local use
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME,
    )


async def upload_weather_data_to_s3(city: str, data: dict, filename: str) -> str:
    async with get_s3_client() as s3_client:
        json_data = json.dumps(data)
        await s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=filename, Body=json_data)
        return f"s3://{S3_BUCKET_NAME}/{filename}"

async def check_s3_cache(city: str) -> dict:
    async with get_s3_client() as s3_client:
        try:
            response = await s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=f"{city}.json")
            content = await response['Body'].read()
            return json.loads(content)
        except s3_client.exceptions.NoSuchKey:
            return None
        except Exception as e:
            print(f"Error fetching from S3: {e}")
            return None
