import enum
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, BigInteger, DECIMAL, Integer, String, TIMESTAMP, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OrderStatusEnum(enum.Enum):
    # Define the possible account types here
    OPEN = "OPEN"
    CLOSE = "CLOSE"


class EventOrder(Base):
    __tablename__ = 'event_order'

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    open_price = Column(DECIMAL(50, 15), nullable=True, comment='开仓价格')
    close_price = Column(DECIMAL(50, 15), nullable=True, comment='平仓价格')
    fee = Column(DECIMAL(12, 4), nullable=True, comment='手续费')
    fee_rate = Column(DECIMAL(12, 6), nullable=True, comment='手续费率')
    buy_amount = Column(DECIMAL(30, 6), nullable=True, comment='买入金额')
    profit = Column(DECIMAL(30, 6), nullable=True, comment='收益')
    create_time = Column(TIMESTAMP, nullable=True, comment='创建时间')
    open_time = Column(TIMESTAMP, nullable=True, comment='开单时间')
    close_time = Column(TIMESTAMP, nullable=True, comment='开单时间')
    close_trigger_time = Column(TIMESTAMP, nullable=True, comment='平仓触发时间')
    intervals = Column(Integer, nullable=True, comment='平仓周期')
    user_id = Column(BigInteger, nullable=True, comment='开单用户')
    base_coin = Column(String(255), nullable=True, comment='开单币种')
    status = Column(Enum(OrderStatusEnum), nullable=True, comment='订单状态')

    def __repr__(self):
        return f"<EventOrder(id={self.id}, base_coin={self.base_coin}, profit={self.profit})>"


class OrderParam(BaseModel):
    intervals: Optional[int] = None
    baseCoin: Optional[str] = None
    buyAmount: Optional[Decimal] = None
