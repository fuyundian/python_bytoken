# 具体实现 UserService 的类

from bytoken.org.common.db.mysqldb import SessionLocal
from bytoken.org.common.db.mysqldb.AbstractWrapper import AbstractWrapper
from bytoken.org.model.User import User
from bytoken.org.service.UserService import UserService


class UserServiceImpl(UserService):
    def __init__(self):
        session = SessionLocal()
        self.service = AbstractWrapper(User, session)

    def getUserById(self, user_id: int) -> User:
        user = self.service.lambdaQuery().eq(user_id > 0, User.id, user_id).one()
        return user
