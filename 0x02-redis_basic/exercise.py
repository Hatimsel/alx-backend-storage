#!/usr/bin/env python3
"""
Writing strings to redis
"""
import redis
from typing import Any
import uuid


class Cache:
    """Cache class"""
    def __init__(self):
        """Intantiating our class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """sets a key/value pair in redis and returns the key"""
        key = str(uuid.uuid1())
        self._redis.set(key, data)

        return key
