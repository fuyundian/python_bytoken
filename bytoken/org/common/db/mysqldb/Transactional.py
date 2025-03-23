import logging
from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from bytoken.org.common.db.mysqldb import getSession

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def Transactional(func):
    """事务管理装饰器，支持回滚"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        session: Session = getSession()
        try:
            logging.info(f"🔄 开始事务: {func.__name__}")
            result = func(*args, **kwargs)

            # 检查事务是否已提交或回滚
            if session.is_active:
                session.commit()
                logging.info(f"✅ 事务提交成功: {func.__name__}")
            return result
        except SQLAlchemyError as e:
            if session.is_active:
                session.rollback()
                logging.error(f"❌ 事务回滚 (SQLAlchemyError): {func.__name__} - {e}")
            raise e
        except Exception as e:
            if session.is_active:
                session.rollback()
                logging.error(f"❌ 事务回滚 (Exception): {func.__name__} - {e}")
            raise e
        finally:
            session.close()
            logging.info(f"🔒 事务已关闭: {func.__name__}")

    return wrapper
