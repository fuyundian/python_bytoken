import decimal
from abc import ABC, abstractmethod

from bytoken.org.model.UserAsset import UserAsset, UserAssetParam


class UserAssetService(ABC):

    # 获取用户资产
    @abstractmethod
    def get_user_asset(self, user_id: int, coin: str) -> UserAsset:
        pass

    @abstractmethod
    def deposition(self, user_id: int, param: UserAssetParam):
        pass

    @abstractmethod
    def lock(self, user_id: int, coin: str, lockAmount: decimal.Decimal):
        pass

    @abstractmethod
    def incBalance(self, user_id: int, coin: str, amount: decimal.Decimal):
        pass
