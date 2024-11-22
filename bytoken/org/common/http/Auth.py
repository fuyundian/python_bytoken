import jwt

from bytoken.org.config import secret_key, algorithm


def getUserId(request) -> int:
    authKey = request.headers.get("Authorization")
    if authKey is None:
        return None
    authKey = authKey.replace("Bearer ", "").replace("bearer ", "")
    payload = jwt.decode(authKey, secret_key, algorithms=[algorithm])
    return payload["user_id"]
