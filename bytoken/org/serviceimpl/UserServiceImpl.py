# 具体实现 UserService 的类
import string
from datetime import timedelta, datetime

import bcrypt
import jwt

from bytoken.org.common.cache import getCache
from bytoken.org.common.db.mysqldb import SessionLocal
from bytoken.org.common.db.mysqldb.AbstractWrapper import AbstractWrapper
from bytoken.org.config import secret_key, access_token_expire_minutes, algorithm
from bytoken.org.model.User import User
from bytoken.org.service.UserService import UserService


class UserServiceImpl(UserService):
    def __init__(self):
        session = SessionLocal()
        self.service = AbstractWrapper(User, session)

    def getUserById(self, user_id: int) -> User:
        user = self.service.lambdaQuery().eq(user_id > 0, User.id, user_id).one()
        user.password = None
        return user

    def login(self, loginParam) -> string:
        if (loginParam.email is None or loginParam.password is None or loginParam.email == ""
                or loginParam.password == ""):
            raise ValueError("Parameter error")
        user = self.service.lambdaQuery().eq(loginParam.email != "", User.email, loginParam.email).one()
        if user is None:
            raise ValueError("User not found")
        if checkPassword(loginParam.password, user.password) is False:
            raise ValueError("Wrong user or password")
        token = createToken(data=user)
        redis_client = getCache().redis_client
        redis_client.set("python_user_token:" + user.id, token, access_token_expire_minutes)
        return token


def checkPassword(password: str, userPassword: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), userPassword.encode('utf-8'))


# JWT 生成器函数
def createToken(data: dict):
    # 检查 data 是否为 None 或非字典
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt
