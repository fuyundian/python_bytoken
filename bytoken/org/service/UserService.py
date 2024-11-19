import string
from abc import ABC, abstractmethod

from bytoken.org.model.User import User, UserLoginParam


class UserService(ABC):
    @abstractmethod
    def getUserById(self, userId: int) -> User:
        pass

    @abstractmethod
    def login(self, loginParam: UserLoginParam) -> string:
        pass
