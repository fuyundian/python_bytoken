import threading
import time
import uuid

import redis


# 锁未获取异常
class LockNotObtained(Exception):
    pass


# 默认超时时间
UNLOCK_MESSAGE = "unlock"
DEFAULT_WATCHDOG_TIMEOUT = 30000  # 30 seconds


def current_time_millis():
    """获取当前时间的毫秒数"""
    return int(time.time() * 1000)


class Redisson:
    def __init__(self, redis_url="redis://localhost:6379/0", watch_dog_timeout=30000):
        self.c = redis.StrictRedis.from_url(redis_url)
        self.watch_dog_timeout = watch_dog_timeout
        self.uuid = str(uuid.uuid4())
        self.renew_map = {}

    def get_channel_name(self, key):
        return f"redisson_channel:{key}"

    def get_entry_name(self, key):
        return f"redisson_entry:{key}"


class RLock:
    def __init__(self, key, g: Redisson):
        self.key = key
        self.g = g

    def lock(self):
        """阻塞获取锁"""
        return self.try_lock(-1, -1)

    def try_lock(self, wait_time, lease_time):
        """尝试获取锁"""
        wait = wait_time
        current = current_time_millis()
        ttl = self.try_acquire(lease_time)

        if ttl == 0:
            return True
        wait -= current_time_millis() - current

        if wait <= 0:
            raise LockNotObtained("Lock not obtained")

        pubsub = self.g.c.pubsub()
        pubsub.subscribe(self.g.get_channel_name(self.key))

        while wait > 0:
            current = current_time_millis()
            try:
                ttl = self.try_acquire(lease_time)
                if ttl == 0:
                    return True
            except Exception as e:
                continue

            wait -= current_time_millis() - current
            if wait <= 0:
                raise LockNotObtained("Lock not obtained")

            try:
                message = pubsub.get_message(timeout=wait / 1000.0)
                if message:
                    break
            except Exception as e:
                continue

        return False

    def try_acquire(self, lease_time):
        """尝试获取锁的内部实现"""
        lock_name = self.get_hash_key(threading.get_ident())
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

    def unlock(self):
        """释放锁"""
        lock_name = self.get_hash_key(threading.get_ident())
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
        result = self.g.c.eval(script, 2, self.key, self.g.get_channel_name(self.key), UNLOCK_MESSAGE,
                               DEFAULT_WATCHDOG_TIMEOUT, lock_name)
        return int(result)

    def get_hash_key(self, thread_id):
        """生成唯一的哈希键"""
        return f"{self.g.uuid}:{thread_id}"
