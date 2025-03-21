from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from bytoken.org.config import config

_session_cache = {}


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


def getSession() -> Session:
    # 生成缓存键
    cache_key = getDatabaseUrl(config)

    # 如果已有缓存，则直接返回
    if cache_key in _session_cache:
        return _session_cache[cache_key]

    # 创建 SQLAlchemy 引擎和会话
    engine = createDbEngine(config)
    # 设置会话
    session = sessionmaker(bind=engine, autoflush=False, autocommit=False)()
    # 缓存会话工厂
    _session_cache[cache_key] = session
    return session
