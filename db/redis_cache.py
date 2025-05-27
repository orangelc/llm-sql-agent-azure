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
def get_cache_key(question: str) -> str:
    return "q:" + hashlib.md5(question.encode()).hexdigest()

@async_timeit
def get_cached_answer(question: str) -> str | None:
    return await r.get(get_cache_key(question))

@async_timeit
def set_cached_answer(question: str, answer: str):
    await r.set(get_cache_key(question), answer, ex=3600)

