import numbers
from typing import TypeVar, Generic, Callable

from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# 定义一个类型变量 T，用于指定模型类型
T = TypeVar('T')


class UpdateWrapper(Generic[T]):
    def __init__(self, model: T, session: Session):
        self.model = model  # 要更新的模型
        self.session = session  # 数据库会话
        self.query = session.query(model)  # 初始查询对象
        self.update_values = {}  # 存储要更新的字段和对应的值

    def set(self, update: bool, field, value):
        """设置更新字段和值"""
        if update is True:
            self.update_values[field] = value
        return self

    def eq(self, query: bool, field, value):
        """等于条件"""
        if query is True:
            self.query = self.query.filter(field == value)
        return self

    def in_(self, query: bool, field, values):
        """包含条件（IN）"""
        if query is True:
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

    def update(self):
        """执行更新操作"""
        if not self.update_values:
            raise ValueError("No values to update.")
            # 使用 SQLAlchemy 的 update() 方法进行批量更新
        stmt = update(self.model).where(self.query.whereclause).values(self.update_values)
        self.session.execute(stmt)
        self.session.commit()

    def lambda_update(self, field: str, func: Callable):
        """使用 Lambda 表达式进行字段更新"""
        # Lambda 表达式通常会返回一个新的值，用来更新字段
        self.update_values[field] = func(field)
        return self

    def increment(self, isUpdate: bool, field: str, value: numbers.Number = 1):
        if not hasattr(self.model, field.key):
            raise ValueError(f"Field '{field.key}' does not exist in model '{self.model.__tablename__}'")

        if isUpdate is True:
            # 这里使用 SQLAlchemy 的 func 进行字段自增
            self.update_values[field] = getattr(self.model, field) + value
        return self
