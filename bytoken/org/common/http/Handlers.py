from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from bytoken.org.common.http import Anonymous
from bytoken.org.common.http.Anonymous import verifyToken
from bytoken.org.common.res.DataRes import DataRes


# 捕获 HTTPException
async def httpExceptionHandler(exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        DataRes(
            code=exc.status_code,
            message=exc.detail
        ).dict()
    )


# 捕获其他异常
async def generalExceptionHandler(exc: Exception) -> JSONResponse:
    return JSONResponse(
        DataRes(
            code=500,
            message=str(exc)
        ).dict()
    )


async def validationExceptionHandler(exc: RequestValidationError):
    return JSONResponse(
        DataRes(
            code=400,
            message=str(exc)
        ).dict()
    )


# 自定义鉴权处理器
async def authenticateRequestMiddleware(request: Request, call_next):
    if any(isinstance(dep, Anonymous) for dep in request.scope.get("dependencies", [])):
        response = await call_next(request)
        return response
    authKey = request.headers.get("Authorization")
    if authKey is None:
        return None
    authKey = authKey.replace("Bearer ", "").replace("bearer ", "")
    if verifyToken(authKey) is False:
        raise HTTPException(status_code=403, detail="Unauthorized")
    response = await call_next(request)
    return response
