# 定义一个空的依赖，用来标记不需要鉴权的接口
class Anonymous:
    def __init__(self):
        self.name = "Anonymous User"


def getAnonymous() -> Anonymous:
    return Anonymous()
