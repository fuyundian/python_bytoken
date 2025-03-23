# containers.py
from dependency_injector import containers, providers

from bytoken.org.service.EventOrderService import EventOrderService
from bytoken.org.service.QuotesService import QuotesService
from bytoken.org.service.UserAssetService import UserAssetService
from bytoken.org.service.UserService import UserService
from bytoken.org.serviceimpl.EventOrderServiceImpl import EventOrderServiceImpl
from bytoken.org.serviceimpl.QuotesServiceImpl import QuotesServiceImpl
from bytoken.org.serviceimpl.UserAssetServiceImpl import UserAssetServiceImpl
from bytoken.org.serviceimpl.UserServiceImpl import UserServiceImpl


class Container(containers.DeclarativeContainer):
    userService = providers.Singleton(UserServiceImpl)
    userAssetService = providers.Singleton(UserAssetServiceImpl)
    quotesService = providers.Singleton(QuotesServiceImpl)
    eventOrderService = providers.Singleton(EventOrderServiceImpl)


def getUserService() -> UserService:
    # 直接从容器获取 UserServiceImpl 实例
    return Container.userService()


def getEventOrderService() -> EventOrderService:
    return Container.eventOrderService()


def getUserAssetService() -> UserAssetService:
    # 直接从容器获取 UserServiceImpl 实例
    return Container.userAssetService()


def getQuotesService() -> QuotesService:
    # 直接从容器获取 UserServiceImpl 实例
    return Container.quotesService()
