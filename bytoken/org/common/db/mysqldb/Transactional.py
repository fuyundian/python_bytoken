import logging
from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def Transactional(func):
    """事务管理装饰器，支持回滚"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 优先使用传入的 session 参数，否则尝试从对象属性中获取
        session: Session = kwargs.get("session")
        if not session and len(args) > 0:
            # 如果方法属于某个类，尝试获取 self.session
            instance = args[0]
            session = getattr(instance, "session", None)
        if not session:
            raise ValueError("缺少数据库会话对象 (session)")

        try:
            logger.info(f"开始事务：{func.__name__}")
            result = func(*args, **kwargs)

            # 检查事务是否已提交或回滚过
            if session.is_active:
                session.commit()
                logger.info(f"事务成功提交：{func.__name__}")
            else:
                logger.warning(f"事务已提交或回滚，无需再次提交：{func.__name__}")

            return result
        except SQLAlchemyError as e:
            if session.is_active:
                session.rollback()
                logger.error(f"SQLAlchemy 异常，事务回滚：{func.__name__}，原因：{e}")
            else:
                logger.error(f"SQLAlchemy 异常，事务已回滚：{func.__name__}，原因：{e}")
            raise
        except Exception as e:
            if session.is_active:
                session.rollback()
                logger.error(f"未知异常，事务回滚：{func.__name__}，原因：{e}")
            else:
                logger.error(f"未知异常，事务已回滚：{func.__name__}，原因：{e}")
            raise

    return wrapper
