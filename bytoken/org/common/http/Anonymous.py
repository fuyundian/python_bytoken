# 定义一个空的依赖，用来标记不需要鉴权的接口
from datetime import time
from http.client import HTTPException

import jwt

from bytoken.org.config import secret_key, algorithm


class Anonymous:
    def __init__(self):
        self.name = "Anonymous User"


def getAnonymous() -> Anonymous:
    return Anonymous()


# 用于验证用户身份的函数
def verifyToken(token: str) -> bool:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
    return payload.get("exp").timestamp() < time.time()


