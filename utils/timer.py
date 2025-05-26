import time
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def async_timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        logger.info(f"async {func.__name__} ejecutado en {duration:.3f}s")
        return result
    return wrapper
