import os

# General settings
API_OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
API_OPENWEATHER_KEY = os.getenv("API_OPENWEATHER_KEY")

if not API_OPENWEATHER_KEY:
    raise ValueError("API_OPENWEATHER_KEY is not set")

# AWS/LocalStack settings
LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localstack:4566")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "test")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "test")
REGION_NAME = os.getenv("REGION_NAME", "us-east-1")

# S3 settings
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "weather-bucket")

# DynamoDB settings
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "WeatherLogs")

# Cache settings
CACHE_EXPIRY_SECONDS = int(os.getenv("CACHE_EXPIRY_SECONDS", 300))  # 5 minutes

# Redis settings
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")