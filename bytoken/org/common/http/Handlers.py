from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

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

# app.add_middleware(CustomInterceptorMiddleware)
