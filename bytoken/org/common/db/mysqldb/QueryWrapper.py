from typing import TypeVar, Generic, List

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

# 定义一个类型变量 T，用于指定模型类型
T = TypeVar('T')


class QueryWrapper(Generic[T]):
    def __init__(self, model: T, session: Session):
        self.model = model  # 要查询的模型
        self.session = session  # 数据库会话
        self.query = session.query(model)  # 初始查询对象

    def eq(self, query: bool, field, value):
        """等于条件"""
        if query is True:
            self.query = self.query.filter(field == value)
        return self

    def in_(self, query: bool, field, values):
        """包含条件（IN）"""
        self.query = self.query.filter(field.in_(values))
        return self

    def nin(self, query: bool, field, values):
        """不包含条件（NOT IN）"""
        if query is True:
            self.query = self.query.filter(~field.in_(values))
        return self

    def like(self, query: bool, field, value):
        """LIKE 查询"""
        if query is True:
            self.query = self.query.filter(field.like(f"%{value}%"))
        return self

    def not_like(self, query: bool, field, value):
        """NOT LIKE 查询"""
        if query is True:
            self.query = self.query.filter(~field.like(f"%{value}%"))
        return self

    def order_by(self, query: bool, *args, ascending=True):
        """排序方法，支持升序和降序"""
        if query is True:
            ordering = [asc(arg) if ascending else desc(arg) for arg in args]
            self.query = self.query.order_by(*ordering)
        return self

    def page(self, page, page_size):
        """分页方法"""
        offset = (page - 1) * page_size
        self.query = self.query.offset(offset).limit(page_size)
        return self

    def list(self) -> List[T]:
        """执行查询并返回所有结果"""
        return self.query.all()

    def one(self) -> T:
        """执行查询并返回第一个结果"""
        return self.query.first()

    def count(self) -> int:
        """返回查询结果的总记录数"""
        return self.query.count()

    def select(self, *fields):
        """选择特定字段"""
        self.query = self.query.with_entities(*fields)
        return self
