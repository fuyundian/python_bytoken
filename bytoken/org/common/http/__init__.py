from typing import AsyncGenerator

import jwt
from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer

from bytoken.org.common.cache import getCache
from bytoken.org.common.db.mysqldb import SessionLocal
from bytoken.org.common.http.Anonymous import Anonymous
from bytoken.org.common.http.Handlers import httpExceptionHandler, authenticateRequestMiddleware, \
    generalExceptionHandler, validationExceptionHandler
from bytoken.org.controller import UserController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 创建自定义异步上下文管理器
class LifespanManager:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __aenter__(self):
        # 启动时的初始化操作（例如连接数据库或 Redis）
        print("Application started, initializing resources...")
        # 这里可以初始化资源，例如连接到数据库或 Redis
        return self  # 返回自己

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 应用关闭时的清理操作
        print("Application shutdown, closing resources...")
        await getCache().redis_client.close()
        await SessionLocal.close_all()


async def lifespan(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        yield


app = FastAPI(lifespan=lifespan)
app.middleware(authenticateRequestMiddleware)
app.add_exception_handler(handler=httpExceptionHandler, exc_class_or_status_code=HTTPException)
app.add_exception_handler(handler=generalExceptionHandler, exc_class_or_status_code=RequestValidationError)
app.add_exception_handler(handler=validationExceptionHandler, exc_class_or_status_code=Exception)
app.include_router(UserController.router, prefix="/user", tags=["user"])
