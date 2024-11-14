# containers.py
from dependency_injector import containers, providers

from bytoken.org.serviceimpl.UserServiceImpl import UserServiceImpl


class Container(containers.DeclarativeContainer):
    userService = providers.Singleton(UserServiceImpl)


def getUserService():
    return Container().userService()
