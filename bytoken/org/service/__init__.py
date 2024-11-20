# containers.py
from dependency_injector import containers, providers

from bytoken.org.service.UserService import UserService
from bytoken.org.serviceimpl.UserServiceImpl import UserServiceImpl


class Container(containers.DeclarativeContainer):
    userService = providers.Singleton(UserServiceImpl)


def getUserService() -> UserService:
    # 直接从容器获取 UserServiceImpl 实例
    return Container.userService()