# 定义一个类型变量 T，用于指定模型类型
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from bytoken.org.common.db.mysqldb.QueryWrapper import QueryWrapper
from bytoken.org.common.db.mysqldb.UpdateWrapper import UpdateWrapper

T = TypeVar('T')


class AbstractWrapper(Generic[T]):
    def __init__(self, model: T, session: Session):
        self.model = model  # 要查询的模型
        self.session = session  # 数据库会话
        self.query = QueryWrapper(self.model, session)
        self.update = UpdateWrapper(self.model, session)

    def lambdaQuery[T](self) -> QueryWrapper[T]:
        return self.query

    def lambdaUpdate[T](self) -> UpdateWrapper[T]:
        return self.update
