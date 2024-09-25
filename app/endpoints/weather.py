from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from app.handlers.weather import get_weather_data, CityNotFoundException
from app.s3_client import upload_weather_data_to_s3, check_s3_cache
from app.dynamodb_client import log_event_to_dynamodb
from app.utils import get_current_timestamp
from fastapi_cache.decorator import cache


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str

router = APIRouter()

@router.get("/{city}/")
@cache(expire=60) 
async def get_weather(city: str):
    try:
        weather_data = await get_weather_data(city)
    except CityNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Store weather data in S3 (or local equivalent)
    timestamp = get_current_timestamp()
    filename = f"{city}_{timestamp}.json"
    s3_url = await upload_weather_data_to_s3(city, weather_data, filename)
    
    # Log the event in DynamoDB (or local equivalent)
    await log_event_to_dynamodb(city, timestamp, s3_url)

    return weather_data
