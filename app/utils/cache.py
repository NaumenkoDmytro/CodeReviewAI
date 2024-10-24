import aioredis
import json
from app.settings import REDIS_URL
from typing import Any, Optional

redis = aioredis.from_url(REDIS_URL)


def generate_cache_key(key_prefix: str, *args) -> str:
    """
    Generates a cache key by concatenating the key prefix with additional arguments.

    Parameters:
    key_prefix (str): The prefix for the cache key.
    args (str): Additional arguments to append to the cache key, separated by colons.

    Returns:
    str: A formatted cache key in the format "key_prefix:arg1:arg2:...".
    """
    return f"{key_prefix}:" + ":".join(args)


async def get_cached_data(key: str) -> Optional[Any]:
    """
    Retrieves cached data for the given key from the Redis cache.

    Parameters:
    key (str): The cache key to retrieve data for.

    Returns:
    Optional[Any]: The cached data, if found, deserialized from JSON format. Returns None if the key is not found.
    """
    cached_value = await redis.get(key)
    if cached_value:
        return json.loads(cached_value)
    return None


async def set_cached_data(key: str, value: Any, ttl: int = 600) -> None:
    """
    Sets data in the Redis cache with an optional time-to-live (TTL).

    Parameters:
    key (str): The cache key to set.
    value (Any): The data to cache, which will be serialized to JSON.
    ttl (int, optional): Time-to-live (TTL) in seconds for the cached data. Defaults to 600 seconds.

    Returns:
    None
    """
    await redis.set(key, json.dumps(value), ex=ttl)
