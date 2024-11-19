# containers.py
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

from bytoken.org.service.UserService import UserService
from bytoken.org.serviceimpl.UserServiceImpl import UserServiceImpl


class Container(containers.DeclarativeContainer):
    userService = providers.Singleton(UserServiceImpl)


@inject
def getUserService(userService: UserService = Provide[Container.userService]) -> UserService:
    return userService
