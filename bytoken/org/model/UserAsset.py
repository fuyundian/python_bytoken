import enum
from typing import Optional

from openai import BaseModel
from sqlalchemy import Column, String, BigInteger, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AccountTypeEnum(enum.Enum):
    # Define the possible account types here
    SPOT = "SPOT"
    FUTURES = "FUTURES"
    # Add more types as needed


class UserAsset(Base):
    __tablename__ = 'user_asset'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    account_type = Column(Enum(AccountTypeEnum), nullable=False)
    coin = Column(String(20), nullable=False)
    balance = Column(Numeric(20, 8), nullable=False, default=0)
    available = Column(Numeric(20, 8), nullable=False, default=0)
    freeze = Column(Numeric(20, 8), nullable=False, default=0)
    locked = Column(Numeric(20, 8), nullable=False, default=0)

    def __repr__(self):
        return f"<UserAsset(id={self.id}, account_id={self.user_id}, account_type={self.account_type}, coin={self.coin}, balance={self.balance})>"


class UserAssetParam(BaseModel):
    coin: Optional[str] = None
    amount: Optional[int] = None
