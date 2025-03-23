from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer

from bytoken.org.common.cache import getCache
from bytoken.org.common.db.mysqldb import getSession
from bytoken.org.common.exe.ParamException import ParamException
from bytoken.org.common.http.Anonymous import Anonymous
from bytoken.org.common.http.Handlers import httpExceptionHandler, authenticateRequestMiddleware, \
    generalExceptionHandler, validationExceptionHandler, paramExceptionHandler
from bytoken.org.controller import UserController, UserAssetController, EventOrderController
from bytoken.org.service import getQuotesService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 创建自定义异步上下文管理器
class LifespanManager:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __aenter__(self):
        # 启动时的初始化操作（例如连接数据库或 Redis）
        print("Application started, initializing resources...")
        # 这里可以初始化资源，例如连接到数据库或 Redis
        getQuotesService().init()
        return self  # 返回自己

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # 应用关闭时的清理操作
        print("Application shutdown, closing resources...")
        await getCache().close()
        await getQuotesService().exit()
        getSession().close()


async def lifespan(app: FastAPI) -> AsyncGenerator:
    async with LifespanManager(app):
        yield


app = FastAPI(lifespan=lifespan)
app.middleware(authenticateRequestMiddleware)
app.add_exception_handler(exc_class_or_status_code=ParamException, handler=paramExceptionHandler)
app.add_exception_handler(handler=httpExceptionHandler, exc_class_or_status_code=HTTPException)
app.add_exception_handler(handler=validationExceptionHandler, exc_class_or_status_code=RequestValidationError)
app.add_exception_handler(handler=generalExceptionHandler, exc_class_or_status_code=Exception)
app.include_router(UserController.router, prefix="/user", tags=["user"])
app.include_router(UserAssetController.router, prefix="/userAsset", tags=["userAsset"])
app.include_router(EventOrderController.router, prefix="/order", tags=["order"])
