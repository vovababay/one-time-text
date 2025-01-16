import os
from aiocache import Cache

CACHE_BACKEND = os.getenv("CACHE_BACKEND", "memory").lower()

def create_redis_cache():
    return Cache(
        Cache.REDIS,
        endpoint=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None),
    )

def create_memcached_cache():
    return Cache(
        Cache.MEMCACHED,
        endpoint=os.getenv("MEMCACHED_HOST", "localhost"),
        port=int(os.getenv("MEMCACHED_PORT", 11211)),
    )

def create_memory_cache():
    return Cache(Cache.MEMORY)

