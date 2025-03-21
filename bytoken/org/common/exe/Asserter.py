from bytoken.org.common.exe.ParamException import ParamException


class Asserter:

    @staticmethod
    def state(expression: bool, message: str):
        if not expression:
            raise ParamException.error(code=400, message=message)
