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
        pool_size=db.get("pool_size", 5),
        max_overflow=db.get("max_overflow", 10),
        pool_timeout=db.get("pool_timeout", 30),
        pool_recycle=db.get("pool_recycle", 3600),
        pool_pre_ping=db.get("pool_pre_ping", True)
    )

# 创建 SQLAlchemy 引擎和会话
engine = createDbEngine(config)
# 设置会话
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
