import aiohttp
import asyncio
import logging
from app.settings import API_OPENWEATHER_URL, API_OPENWEATHER_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CityNotFoundException(Exception):
    pass

async def get_weather_data(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        params = {"q": city, "appid": API_OPENWEATHER_KEY}
        logger.info(f"Fetching weather data for {city} with params: {params}")
        retries = 3
        for attempt in range(retries):
            try:
                async with session.get(API_OPENWEATHER_URL, params=params, timeout=10) as response:
                    if response.status == 404:
                        raise CityNotFoundException(f"City {city} not found")
                    if response.status != 200:
                        raise Exception(f"Error fetching weather data: {response.status}")
                    return await response.json()
            except asyncio.TimeoutError:
                if attempt < retries - 1:
                    logger.warning(f"Timeout error, retrying... ({attempt + 1}/{retries})")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise Exception("Request timed out after multiple attempts")
            except aiohttp.ClientError as e:
                raise Exception(f"Client error: {e}")
