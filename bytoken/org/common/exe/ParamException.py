class ParamException(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message

    def __code__(self):
        return self.code

    def __message__(self):
        return self.message
