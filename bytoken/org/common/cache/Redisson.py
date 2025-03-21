import threading
import time
import uuid
from typing import Callable, Optional
from bytoken.org.config import redis_host, redis_port, redis_db

import redis

# Default Watchdog Timeout
DEFAULT_WATCHDOG_TIMEOUT = 30  # 30 seconds


# Redis client configuration
def get_redis() -> redis.Redis:
    pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
    redis_client = redis.Redis(connection_pool=pool)
    return redis_client


# Option to configure the pyRedisson
class OptionFunc:
    def __init__(self, func: Callable):
        self.func = func

    def __call__(self, g):
        self.func(g)


# pyRedisson equivalent in Python
class pyRedisson:
    def __init__(self, watch_dog_timeout: Optional[float] = DEFAULT_WATCHDOG_TIMEOUT):
        self.c = get_redis()
        self.uuid = str(uuid.uuid4())  # Unique UUID for the instance
        self.watchDogTimeout = watch_dog_timeout
        self.renew_map = {}  # Using a dictionary instead of cmap.ConcurrentMap

    def get_entry_name(self, key: str) -> str:
        return f"{self.uuid}:{key}"

    def get_channel_name(self, key: str) -> str:
        return f"{{gedisson_lock__channel}}:{key}"

    def new_r_lock(self, key: str) -> 'RLock':
        return RLock(key, self)

    def new_mutex(self, key: str) -> 'Mutex':
        return Mutex(key, self)


# RLock class equivalent
class RLock:
    def __init__(self, key: str, g: pyRedisson):
        self.key = key
        self.g = g

    def lock(self):
        """Blocking lock acquisition."""
        return self.try_lock(-1, -1)

    def try_lock(self, wait_time: int, lease_time: int) -> bool:
        """Try to acquire the lock."""
        wait = wait_time
        current = int(time.time() * 1000)
        ttl = self.try_acquire(lease_time)

        if ttl == 0:
            return True
        wait -= int(time.time() * 1000) - current

        if wait <= 0:
            raise Exception("Lock not obtained")

        pubsub = self.g.c.pubsub()
        pubsub.subscribe(self.g.get_channel_name(self.key))

        while wait > 0:
            current = int(time.time() * 1000)
            ttl = self.try_acquire(lease_time)
            if ttl == 0:
                return True
            wait -= int(time.time() * 1000) - current
            if wait <= 0:
                raise Exception("Lock not obtained")

            message = pubsub.get_message(timeout=wait / 1000.0)
            if message:
                break

        return False

    def try_acquire(self, lease_time: int) -> int:
        """Try to acquire the lock internally."""
        lock_name = self.get_hash_key()
        script = """
        if (redis.call('exists', KEYS[1]) == 0) then
            redis.call('hincrby', KEYS[1], ARGV[2], 1);
            redis.call('pexpire', KEYS[1], ARGV[1]);
            return 0;
        end;
        if (redis.call('hexists', KEYS[1], ARGV[2]) == 1) then
            redis.call('hincrby', KEYS[1], ARGV[2], 1);
            redis.call('pexpire', KEYS[1], ARGV[1]);
            return 0;
        end;
        return redis.call('pttl', KEYS[1]);
        """
        result = self.g.c.eval(script, 1, self.key, lease_time, lock_name)
        return int(result)

    def unlock(self) -> int:
        """Release the lock."""
        lock_name = self.get_hash_key()
        script = """
        if (redis.call('hexists', KEYS[1], ARGV[3]) == 0) then
            return nil;
        end;
        local counter = redis.call('hincrby', KEYS[1], ARGV[3], -1);
        if (counter > 0) then
            redis.call('pexpire', KEYS[1], ARGV[2]);
            return 0;
        else
            redis.call('del', KEYS[1]);
            redis.call('publish', KEYS[2], ARGV[1]);
            return 1;
        end;
        return nil;
        """
        result = self.g.c.eval(script, 2, self.key, self.g.get_channel_name(self.key), "unlock",
                               self.g.watchDogTimeout * 1000, lock_name)
        if result is None:
            return -1  # 可以自定义一个失败码
        return int(result)

    def get_hash_key(self) -> str:
        """Generate unique hash key."""
        return f"{self.g.uuid}:{threading.get_ident()}"


# Mutex class equivalent
class Mutex:
    def __init__(self, key: str, g: pyRedisson):
        self.key = key
        self.g = g


# Global singleton instance of pyRedisson
go_redisson_instance = None


def redisson() -> pyRedisson:
    """Get the global pyRedisson instance.
    :rtype: object
    """
    global go_redisson_instance
    if go_redisson_instance is None:
        go_redisson_instance = pyRedisson()
    return go_redisson_instance
