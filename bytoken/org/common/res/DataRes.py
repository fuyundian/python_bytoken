from typing import Optional, TypeVar

from openai import BaseModel

T = TypeVar('T')


class DataRes(BaseModel):
    def __init__(self, code: int, message: str, data: Optional[T] = None):
        self.code = code
        self.message = message
        self.data = data

    @classmethod
    def success(cls, data: Optional[T] = None) -> "DataRes":
        return cls(code=200, message="Success", data=data)

    @classmethod
    def fail(cls, message: str, code: int = 400) -> "DataRes":
        return cls(code=code, message=message)

    def dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}
