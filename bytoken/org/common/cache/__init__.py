# containers.py
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from bytoken.org.common.cache.Cache import Cache
from bytoken.org.config import redis_host, redis_port, redis_db


class Container(containers.DeclarativeContainer):
    cache = providers.Singleton(Cache, host=redis_host, port=redis_port, db=redis_db)


@inject
def getCache(cache: Cache = Provide[Container.cache]) -> Cache:
    return cache
