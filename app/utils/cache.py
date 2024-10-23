import aioredis
import json
from app.settings import REDIS_URL

redis = aioredis.from_url(REDIS_URL)

# Helper function to generate cache keys based on function inputs
def generate_cache_key(key_prefix: str, *args):
    return f"{key_prefix}:" + ":".join(args)

# Get cached data by key
async def get_cached_data(key: str):
    cached_value = await redis.get(key)
    if cached_value:
        return json.loads(cached_value)
    return None

# Set data in cache with a time-to-live (ttl) in seconds
async def set_cached_data(key: str, value, ttl=600):
    await redis.set(key, json.dumps(value), ex=ttl)