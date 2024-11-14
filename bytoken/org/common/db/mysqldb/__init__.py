from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bytoken.org.config import config


# 解析数据库连接字符串
def getDatabaseUrl(config: dict) -> str:
    db = config["database"]
    return f"{db['driver']}://{db['username']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"


def createDbEngine(config: dict):
    db = config["database"]
    return create_engine(
        getDatabaseUrl(config),
    )


# 创建 SQLAlchemy 引擎和会话
engine = createDbEngine(config)
# 设置会话
SessionLocal = sessionmaker(bind=engine)
