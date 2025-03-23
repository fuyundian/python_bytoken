import decimal

from bytoken.org.common.cache import Redisson
from bytoken.org.common.db.mysqldb import getSession
from bytoken.org.common.db.mysqldb.AbstractWrapper import AbstractWrapper
from bytoken.org.common.db.mysqldb.Transactional import Transactional
from bytoken.org.common.exe.Asserter import Asserter
from bytoken.org.common.exe.ParamException import ParamException
from bytoken.org.model.UserAsset import UserAsset, UserAssetParam
from bytoken.org.service.UserAssetService import UserAssetService


class UserAssetServiceImpl(UserAssetService):

    def __init__(self):
        session = getSession()
        self.service = AbstractWrapper[UserAsset](UserAsset, session)

    def getUserAsset(self, user_id: int, coin: str) -> UserAsset:
        return self.service.lambdaQuery().eq(user_id > 0, UserAsset.user_id, user_id).eq(
            coin is not None and coin != "", UserAsset.coin, coin).one()

    def deposition(self, user_id: int, param: UserAssetParam):
        Asserter.state(param.amount is not None and param.amount > 0, message="deposition amount not null")
        Asserter.state(param.coin is not None and param.coin != "", message="deposition coin not null")
        self.incBalance(user_id=user_id, coin=param.coin, amount=param.amount)

    @Transactional
    def lock(self, user_id: int, coin: str, lockAmount: decimal.Decimal):
        pyRedisson = Redisson.redisson()
        lock = pyRedisson.new_r_lock(f"user_asset_lock:{user_id}")
        try:
            if lock.try_lock(20000, 10000) is True:
                (self.service.lambdaUpdate()
                 .increment(lockAmount is not None and lockAmount > 0, UserAsset.locked.key, lockAmount)
                 .eq(user_id > 0, UserAsset.user_id, user_id)
                 .eq(coin is not None and coin != "", UserAsset.coin, coin)
                 .update())
        except Exception as e:
            raise ParamException.error(message=str(e), code=503)
        finally:
            lock.unlock()

    @Transactional
    def incBalance(self, user_id: int, coin: str, amount: decimal.Decimal):
        pyRedisson = Redisson.redisson()
        lock = pyRedisson.new_r_lock(f"user_asset_lock:{user_id}")
        try:
            if lock.try_lock(20000, 10000) is True:
                (self.service.lambdaUpdate()
                 .increment(amount is not None and amount > 0, UserAsset.available.key, amount)
                 .increment(amount is not None and amount > 0, UserAsset.balance.key, amount)
                 .eq(user_id > 0, UserAsset.user_id, user_id)
                 .eq(coin is not None and coin != "", UserAsset.coin, coin)
                 .update())
        except Exception as e:
            raise ParamException.error(message=str(e), code=503)
        finally:
            lock.unlock()
