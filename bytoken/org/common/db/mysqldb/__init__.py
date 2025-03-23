from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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


_session_cache: Dict[str, Session] = {}


def getSession() -> Session:
    """Creates and retrieves a cached session for the given database configuration."""
    # Generate a unique cache key based on the database URL configuration
    cache_key = getDatabaseUrl(config)

    # Check if a session is already cached for this configuration
    if cache_key in _session_cache:
        session = _session_cache[cache_key]
        # Check if the cached session is still active, otherwise recreate it
        if not session.is_active:
            session.close()  # Close the inactive session
            # Recreate a new session and cache it
            session = createNewSession()
            _session_cache[cache_key] = session
        return session

    # If no cached session, create a new session
    session = createNewSession()
    _session_cache[cache_key] = session
    return session


def createNewSession() -> Session:
    """Helper function to create a new session."""
    # Create the SQLAlchemy engine based on the configuration
    engine = createDbEngine(config)
    # Return a new session bound to the engine
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)()
