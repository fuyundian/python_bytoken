class ParamException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __code__(self):
        return self.code

    def __message__(self):
        return self.message

    def __str__(self):
        return f"Error {self.code}: {self.message}"

    @staticmethod
    def error(message: str, code: int = 400) -> "ParamException":
        return ParamException(code=code, message=message)


def error(message: str, code: int = 400) -> "ParamException":
    return ParamException.error(code=code, message=message)
