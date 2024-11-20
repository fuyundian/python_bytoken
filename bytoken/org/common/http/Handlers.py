from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from fastapi import HTTPException, Request

from bytoken.org.common.http import Anonymous
from bytoken.org.common.res.DataRes import DataRes


# 自定义 HTTPException 处理器
class CustomInterceptorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            if response.status_code >= 400:
                # 处理返回的错误响应
                return JSONResponse(
                    status_code=response.status_code,
                    content=DataRes.fail(code=response.status_code, message="请求失败").dict()
                )
            return response
        except Exception as exc:
            # 捕获异常并返回统一格式
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content=DataRes.fail(
                    code=HTTP_500_INTERNAL_SERVER_ERROR,
                    message="服务器内部错误"
                ).dict()
            )


# 自定义鉴权处理器
async def authenticateRequest(request: Request, call_next):
    print("Dependencies in request scope:", request.scope.get("dependencies", []))
    if any(isinstance(dep, Anonymous) for dep in request.scope.get("dependencies", [])):
        response = await call_next(request)
        return response

    api_key = request.headers.get("Authorization")
    if api_key != "mysecureapikey":
        raise HTTPException(status_code=403, detail="Unauthorized")
    response = await call_next(request)
    return response


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
