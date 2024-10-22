import aioredis

redis = aioredis.from_url("redis://localhost")

async def get_cached_data(key):
    return await redis.get(key)

async def set_cached_data(key, value, ttl=600):
    await redis.set(key, value, ex=ttl)
