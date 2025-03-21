from abc import ABC, abstractmethod

from bytoken.org.model.UserAsset import UserAsset, UserAssetParam


class UserAssetService(ABC):

    # 获取用户资产
    @abstractmethod
    def getUserAsset(self, user_id: int, coin: str) -> UserAsset:
        pass

    @abstractmethod
    def deposition(self, user_id: int, param: UserAssetParam):
        pass
