import redis


class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.redis_client = redis.Redis(connection_pool=self.pool)

    def __enter__(self):
        return self.redis_client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_client.close()
        self.pool.disconnect()
