# utils/timer.py
import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"⏱️ {func.__name__} ejecutado en {duration:.3f}s")
        return result
    return wrapper
