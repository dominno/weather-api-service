from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.endpoints.weather import router as weather_router
from app.settings import REDIS_URL

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_client = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

app.include_router(weather_router, prefix="/weather")