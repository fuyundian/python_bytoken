from abc import ABC, abstractmethod

from bytoken.org.model.User import User


class UserService(ABC):
    @abstractmethod
    def getUserById(self, userId: int) -> User:
        pass
