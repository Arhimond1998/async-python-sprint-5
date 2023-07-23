from functools import wraps
import json

from src.services.redis import redis_client


def redis_cached_async(arg_slice: slice):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate the cache key from the function's arguments.
            key_parts = [func.__name__] + list(map(str, args[arg_slice]))
            key = '-'.join(key_parts)
            result = redis_client.get(key)

            if result is None:
                # Run the function and cache the result for next time.
                value = await func(*args, **kwargs)
                value_json = json.dumps(value)
                redis_client.set(key, value_json)
            else:
                # Skip the function entirely and use the cached value instead.
                value_json = result.decode('utf-8')
                value = json.loads(value_json)

            return value

        return wrapper

    return inner
