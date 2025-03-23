import decimal
from datetime import datetime, timedelta

from bytoken.org.common.cache.Redisson import redisson
from bytoken.org.common.db.mysqldb import getSession
from bytoken.org.common.db.mysqldb.AbstractWrapper import AbstractWrapper
from bytoken.org.common.db.mysqldb.Transactional import Transactional
from bytoken.org.common.exe.Asserter import Asserter
from bytoken.org.common.exe.ParamException import ParamException
from bytoken.org.common.utils import StableCoin
from bytoken.org.model.EventOrder import OrderParam, EventOrder, OrderStatusEnum
from bytoken.org.service.EventOrderService import EventOrderService

feeRate = decimal.Decimal('0.01')


class EventOrderServiceImpl(EventOrderService):

    def __init__(self):
        self.session = getSession()
        self.service = AbstractWrapper[EventOrder](EventOrder, self.session)
        from bytoken.org.service import getUserAssetService, getQuotesService
        self.userAssetService = getUserAssetService()
        self.quotesService = getQuotesService()

    @Transactional
    def postOrder(self, user_id: int, order: OrderParam):
        Asserter.state(expression=order.buyAmount is not None, message="金额不能为空")
        Asserter.state(expression=order.intervals is not None, message="周期不能为空")
        Asserter.state(expression=order.buyBaseCoin is not None, message="支付币种不能为空")
        Asserter.state(expression=order.position is not None, message="下单方向不能")
        Asserter.state(
            expression=order.buyBaseCoin in StableCoin.SupportedCurrencies,
            message="目前支持支付币种：" + ", ".join(StableCoin.SupportedCurrencies)
        )
        pyRedisson = redisson()
        lock = pyRedisson.new_r_lock("order_lock:" + str(user_id))
        try:
            if lock.try_lock(10000, 10000):
                asset = self.userAssetService.getUserAsset(user_id=user_id, coin=order.buyBaseCoin)
                Asserter.state(expression=asset is not None and asset.available >= order.buyAmount + asset.locked,
                               message="余额不足")
                self.userAssetService.lock(user_id=user_id, coin=order.buyBaseCoin, lockAmount=order.buyAmount)
                openPrice = self.quotesService.getPrice(baseCoin='BTC')
                newOrder = EventOrder(
                    open_price=openPrice,
                    fee=feeRate * order.buyAmount,
                    fee_rate=feeRate,
                    buy_amount=order.buyAmount,
                    create_time=datetime.now(),
                    open_time=datetime.now(),
                    close_trigger_time=datetime.now() + timedelta(seconds=order.intervals * 60),
                    intervals=order.intervals,
                    user_id=user_id,
                    status=OrderStatusEnum.OPEN,
                    position=order.position,
                    base_coin=order.buyBaseCoin,
                )
                self.service.save(newOrder)
        except ParamException as e:
            raise e
        except Exception as e:
            raise ParamException.error(str(e))
        finally:
            lock.unlock()
