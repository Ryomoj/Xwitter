import redis.asyncio as redis
from redis.asyncio import ConnectionPool

redis_pool = ConnectionPool.from_url(
    "redis://localhost:6379",
    max_connections=20,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5
)

async def get_redis_client():
    return redis.Redis(connection_pool=redis_pool)