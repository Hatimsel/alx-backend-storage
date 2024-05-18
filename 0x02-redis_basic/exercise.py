#!/usr/bin/env python3
"""
Writing strings to redis
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)

        return method(self, *args, **kwargs)
    return wrapper


def call_history(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


class Cache:
    """Cache class"""
    def __init__(self):
        """Intantiating our class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """sets a key/value pair in redis and returns the key"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)

        return key

    @count_calls
    def get(self, key, fn=None):
        """Converts the data associated to key
        into the desired data type"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    @count_calls
    def get_str(self, key):
        """Converts the data associated with key into str"""
        return self.get(key, lambda d: d.decode("utf-8"))

    @count_calls
    def get_int(self, key):
        """Converts the data associated with key into int"""
        return int(self.get(key))

    def get_count(self, fn):
        """Counts the calls of a method"""
        count = self._redis.get(fn)
        if count:
            return int(count)
        return 0

    def get_history(self, fn):
        """Retrieves the ins and out history of a method"""
        input_key = f"{fn}:inputs"
        output_key = f"{fn}:outputs"
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)
        return {
            "inputs": [i.decode('utf-8') for i in inputs],
            "outputs": [o.decode('utf-8') for o in outputs]
        }

    def replay(self, fn):
        """Retrieves and prints the hsitory of ins and outs
        of a method"""
        history = self.get_history(fn)
        inputs = history['inputs']
        outputs = history['outputs']
        print(f"{fn} was called {len(inputs)} times:")
        for i, (input, output) in enumerate(zip(inputs, outputs)):
            print(f"{fn}(*{input}) -> {output}")
