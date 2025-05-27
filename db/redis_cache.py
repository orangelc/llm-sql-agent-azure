import redis
import hashlib
from utils.timer import async_timeit
import redis.asyncio as redis
import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True
)

@async_timeit
async def get_cache_key(question: str) -> str:
    return "q:" + hashlib.md5(question.encode()).hexdigest()

@async_timeit
async def get_cached_answer(question: str) -> str | None:
    key = await get_cache_key(question)
    return await redis_client.get(key)

@async_timeit
async def set_cached_answer(question: str, answer: str):
    key = await get_cache_key(question)
    await redis_client.set(key, answer, ex=3600)

