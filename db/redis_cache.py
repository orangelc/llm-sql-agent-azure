import redis
import hashlib
import os

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def get_cache_key(question: str) -> str:
    return "q:" + hashlib.md5(question.encode()).hexdigest()

def get_cached_answer(question: str) -> str | None:
    return r.get(get_cache_key(question))

def set_cached_answer(question: str, answer: str):
    r.set(get_cache_key(question), answer, ex=3600)
