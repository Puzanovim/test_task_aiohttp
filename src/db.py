import aioredis
from aiohttp import web


async def set_value(key: str, value: int) -> None:
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    await redis.set(key, value)
    redis.close()
    await redis.wait_closed()


async def get_value(key: str) -> int:
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    value = await redis.get(key, encoding='utf-8')
    redis.close()
    print(type(value))
    await redis.wait_closed()
    if value:
        return int(value)
    else:
        raise web.HTTPException(text="Информации о данном обменном курсе нет в базе")


async def clean_db() -> None:
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    await redis.flushall()
    redis.close()
    await redis.wait_closed()
