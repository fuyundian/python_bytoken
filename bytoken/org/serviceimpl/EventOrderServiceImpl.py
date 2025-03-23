import decimal
from datetime import datetime, timedelta

from bytoken.org.common.cache.Redisson import redisson
from bytoken.org.common.db.mysqldb import getSession
from bytoken.org.common.db.mysqldb.AbstractWrapper import AbstractWrapper
from bytoken.org.common.db.mysqldb.Transactional import Transactional
from bytoken.org.common.exe.Asserter import Asserter
from bytoken.org.common.exe.ParamException import ParamException
from bytoken.org.common.utils import StableCoin
from bytoken.org.model.EventOrder import OrderParam, EventOrder, OrderStatusEnum, PositionEnum
from bytoken.org.service.EventOrderService import EventOrderService

feeRate = decimal.Decimal('0.01')


class EventOrderServiceImpl(EventOrderService):

    def __init__(self):
        self.session = getSession()
        self.service = AbstractWrapper[EventOrder](EventOrder, self.session)

    @Transactional
    def postOrder(self, user_id: int, order: OrderParam):
        Asserter.state(expression=order.buyAmount is not None, message="金额不能为空")
        Asserter.state(expression=order.intervals is not None, message="周期不能为空")
        Asserter.state(expression=order.buyBaseCoin is not None, message="币种不能为空")
        Asserter.state(expression=order.position is not None, message="下单方向不能")
        Asserter.state(
            expression=order.buyBaseCoin in StableCoin.SupportedCurrencies,
            message="目前支持币种：" + ", ".join(StableCoin.SupportedCurrencies)
        )
        pyRedisson = redisson()
        lock = pyRedisson.new_r_lock("order_lock:" + str(user_id))
        try:
            if lock.try_lock(10000, 10000):
                from bytoken.org.service import getUserAssetService, getQuotesService
                asset = getUserAssetService().getUserAsset(user_id=user_id, coin=StableCoin.USDT)
                Asserter.state(expression=asset is not None and asset.available >= order.buyAmount + asset.locked,
                               message="余额不足")
                getUserAssetService().lock(user_id=user_id, coin=StableCoin.USDT, lockAmount=order.buyAmount)
                openPrice = getQuotesService().getPrice(baseCoin=order.buyBaseCoin)
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

    def closeOrders(self, coin: str, price: decimal.Decimal):
        pyRedisson = redisson()
        lock = pyRedisson.new_r_lock("close_order_lock")
        try:
            if lock.try_lock(10000, 10000):
                closeOrders = (self.service.lambdaQuery()
                               .eq(True, EventOrder.base_coin, coin)
                               .eq(True, EventOrder.status, OrderStatusEnum.OPEN)
                               .le(True, EventOrder.close_trigger_time, datetime.now())
                               .list())
                if closeOrders is None or len(closeOrders) == 0:
                    return
                for closeOrder in closeOrders:
                    self.closeOrder(closeOrder, price)

        except Exception as e:
            print(str(e))
        finally:
            lock.unlock()

    def closeOrder(self, order: EventOrder, closePrice: decimal.Decimal):
        if order is None or order.status != OrderStatusEnum.OPEN:
            return
        profit = - (order.buy_amount * (decimal.Decimal('1') - order.fee_rate))
        if (order.open_price > decimal.Decimal(closePrice) and order.position == PositionEnum.SHORT) or (
                order.open_price < decimal.Decimal(closePrice) and order.position == PositionEnum.LONG):
            profit = -profit
        update = (self.service.lambdaUpdate()
                  .set(True, EventOrder.close_time, datetime.now())
                  .set(True, EventOrder.status, OrderStatusEnum.CLOSE)
                  .set(True, EventOrder.close_price, decimal.Decimal(closePrice))
                  .set(True, EventOrder.profit, profit)
                  .eq(True, EventOrder.id, order.id)
                  .update())
        if update is None or update is False:
            return
        from bytoken.org.service import getUserAssetService
        getUserAssetService().incBalance(user_id=order.user_id, coin=StableCoin.USDT, amount=profit)
        getUserAssetService().lock(user_id=order.user_id, coin=StableCoin.USDT, lockAmount=-order.buy_amount)
