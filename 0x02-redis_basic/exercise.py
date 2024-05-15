#!/usr/bin/env python3
"""
Writing strings to redis
"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache class"""
    def __init__(self):
        """Intantiating our class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """sets a key/value pair in redis and returns the key"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)

        return key

    def get(self, key, fn=None):
        """Converts the data associated to key
        into the desired data type"""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key):
        """Converts the data associated with key into str"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key):
        """Converts the data associated with key into int"""
        return int(self.get(key))
