import aioredis


async def set_value(key: str, value: int) -> None:
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    await redis.set(key, value)
    await redis.close()
    await redis.wait_closed()


async def get_value(key: str) -> int:
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    value = await redis.get(key, encoding='utf-8')
    redis.close()
    print(type(value))
    await redis.wait_closed()
    return int(value)


async def clean_db() -> None:
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    await redis.flushall()
    redis.close()
    await redis.wait_closed()


async def main():
    redis = await aioredis.create_redis_pool('redis://127.0.0.1')
    await redis.set('my-key', 'value')
    value = await redis.get('my-key', encoding='utf-8')
    print(value)

    redis.close()
    await redis.wait_closed()
