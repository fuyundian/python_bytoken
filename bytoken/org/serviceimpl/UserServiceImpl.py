# 具体实现 UserService 的类
from typing import List

from bytoken.org.model.User import User
from bytoken.org.service.UserService import UserService

class UserServiceImpl(UserService):
    def __init__(self):

    def getUserById(self, user_id: int) -> List[User]:
        return []
