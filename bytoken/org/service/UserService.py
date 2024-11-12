from abc import ABC, abstractmethod
from typing import List

from bytoken.org.model.User import User


class UserService(ABC):
    @abstractmethod
    def getUserById(self, userId: int) -> List[User]:
        pass
