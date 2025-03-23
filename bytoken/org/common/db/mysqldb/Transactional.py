import logging
from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from bytoken.org.common.db.mysqldb import getSession


def Transactional(func):
    """事务管理装饰器，支持回滚"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 优先使用传入的 session 参数，否则尝试从对象属性中获取
        session: Session = getSession()
        try:
            result = func(*args, **kwargs)

            # 检查事务是否已提交或回滚过
            if session.is_active:
                session.commit()
            return result
        except SQLAlchemyError as e:
            if session.is_active:
                session.rollback()
            raise e
        except Exception as e:
            if session.is_active:
                session.rollback()
            raise e

    return wrapper
