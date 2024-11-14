from typing import Optional, TypeVar

T = TypeVar('T')


class DataRes:
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

    def to_dict(self):
        return {"code": self.code, "message": self.message, "data": self.data}
