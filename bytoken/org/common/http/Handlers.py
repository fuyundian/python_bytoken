from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from bytoken.org.common.exe import ParamException
from bytoken.org.common.http import Anonymous
from bytoken.org.common.http.Anonymous import verify_token
from bytoken.org.common.res.DataRes import DataRes


# 捕获 HTTPException
async def httpExceptionHandler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        DataRes(
            code=exc.status_code,
            message=exc.detail
        ).dict()
    )


# 捕获其他异常
async def generalExceptionHandler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        DataRes(
            code=500,
            message=str(exc)
        ).dict()
    )


async def validationExceptionHandler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        DataRes(
            code=400,
            message=str(exc)
        ).dict()
    )


async def paramExceptionHandler(request: Request, exc: ParamException) -> JSONResponse:
    return JSONResponse(
        DataRes(
            code=exc.code,
            message=exc.message
        ).dict()
    )


# 自定义鉴权处理器
async def authenticateRequestMiddleware(request: Request, call_next):
    allowed_paths = ["/docs", "/html", "/css", "/openapi.json"]

    # 如果请求路径以这些前缀开头，直接跳过验证
    if any(request.url.path.startswith(path) for path in allowed_paths):
        return await call_next(request)
    # 允许跳过认证的路径前缀
    if any(isinstance(dep, Anonymous) for dep in request.scope.get("dependencies", [])):
        response = await call_next(request)
        return response
    authKey = request.headers.get("Authorization")
    if authKey is None:
        raise ParamException.error(code=403, message="未登录")
    authKey = authKey.replace("Bearer ", "").replace("bearer ", "")
    if verify_token(authKey) is False:
        raise ParamException.error(code=403, message="Token无效")
    response = await call_next(request)
    return response
