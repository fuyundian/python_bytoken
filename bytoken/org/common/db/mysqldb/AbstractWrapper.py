# 定义一个类型变量 T，用于指定模型类型
from typing import Generic, TypeVar, List

from sqlalchemy.orm import Session

from bytoken.org.common.db.mysqldb import createNewSession
from bytoken.org.common.db.mysqldb.QueryWrapper import QueryWrapper
from bytoken.org.common.db.mysqldb.UpdateWrapper import UpdateWrapper

T = TypeVar('T')


class AbstractWrapper(Generic[T]):
    def __init__(self, model: T, session: Session):
        self.model = model  # 要查询的模型
        self.session = session  # 数据库会话
        self.query = QueryWrapper(self.model, session)

    def lambdaQuery(self) -> QueryWrapper[T]:
        return QueryWrapper(self.model, createNewSession())

    def lambdaUpdate(self) -> UpdateWrapper[T]:
        return UpdateWrapper(self.model, createNewSession())

    def save(self, entity: T) -> bool:
        self.session = createNewSession()
        """保存单个对象"""
        self.session.add(entity)
        self.session.commit()
        return True


def batch_save(self, entities: List[T]) -> bool:
    self.session = createNewSession()
    """批量保存多个对象"""
    self.session.add_all(entities)
    self.session.commit()
    return True


def save_or_update(self, entity: T, primary_key: str = "id") -> bool:
    self.session = createNewSession()
    existing = self.session.query(self.model).get(getattr(entity, primary_key))
    if existing:
        for key, value in vars(entity).items():
            if hasattr(existing, key):
                setattr(existing, key, value)
        self.session.merge(existing)
    else:
        self.session.add(entity)
    self.session.commit()
    return True
