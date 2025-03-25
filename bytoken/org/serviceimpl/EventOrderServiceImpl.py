import decimal
from datetime import datetime, timedelta

from bytoken.org.common.cache.Redisson import redisson
from bytoken.org.common.db.mysqldb import getSession
from bytoken.org.common.db.mysqldb.AbstractWrapper import AbstractWrapper
from bytoken.org.common.db.mysqldb.Transactional import Transactional
from bytoken.org.common.exe.Asserter import Asserter
from bytoken.org.common.exe.ParamException import ParamException
from bytoken.org.common.utils import StableCoin
from bytoken.org.common.utils.ResultPage import ResultPage
from bytoken.org.model.EventOrder import OrderParam, EventOrder, OrderStatusEnum, PositionEnum
from bytoken.org.service.EventOrderService import EventOrderService

feeRate = decimal.Decimal('0.01')


class EventOrderServiceImpl(EventOrderService):

    def __init__(self):
        self.session = getSession()
        self.service = AbstractWrapper[EventOrder](EventOrder, self.session)

    @Transactional
    def post_order(self, user_id: int, order: OrderParam):
        Asserter.state(expression=order.amount is not None, message="金额不能为空")
        Asserter.state(expression=order.intervals is not None, message="周期不能为空")
        Asserter.state(expression=order.base_coin is not None, message="币种不能为空")
        Asserter.state(expression=order.position is not None, message="下单方向不能为空")
        Asserter.state(
            expression=order.base_coin in StableCoin.SupportedCurrencies,
            message="目前支持币种：" + ", ".join(StableCoin.SupportedCurrencies)
        )
        pyRedisson = redisson()
        lock = pyRedisson.new_r_lock("order_lock:" + str(user_id))
        try:
            if lock.try_lock(10000, 10000):
                from bytoken.org.service import getUserAssetService, getQuotesService
                asset = getUserAssetService().get_user_asset(user_id=user_id, coin=StableCoin.USDT)
                Asserter.state(expression=asset is not None and asset.available >= order.amount + asset.locked,
                               message="余额不足")
                open_price = getQuotesService().get_price(baseCoin=order.base_coin)
                Asserter.state(open_price is not None and decimal.Decimal(open_price) > 0, message="当前开仓价格不是最新的")
                getUserAssetService().lock(user_id=user_id, coin=StableCoin.USDT, lockAmount=order.amount)
                newOrder = EventOrder(
                    open_price=open_price,
                    fee=feeRate * order.amount,
                    fee_rate=feeRate,
                    buy_amount=order.amount,
                    create_time=datetime.now(),
                    open_time=datetime.now(),
                    close_trigger_time=datetime.now() + timedelta(seconds=order.intervals * 60),
                    intervals=order.intervals,
                    user_id=user_id,
                    status=OrderStatusEnum.OPEN,
                    position=order.position,
                    base_coin=order.base_coin,
                )
                self.service.save(newOrder)
        except ParamException as e:
            raise e
        except Exception as e:
            raise ParamException.error(str(e))
        finally:
            lock.unlock()

    def close_orders(self, coin: str, price: decimal.Decimal):
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
        base_profit = order.buy_amount * (decimal.Decimal('1') - order.fee_rate)
        profit = base_profit
        if (order.open_price < decimal.Decimal(closePrice) and order.position == PositionEnum.SHORT) or (
                order.open_price > decimal.Decimal(closePrice) and order.position == PositionEnum.LONG):
            profit = - base_profit
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

    def order_pages(self, user_id: int, param: OrderParam) -> ResultPage[EventOrder]:
        return self.service.lambdaQuery() \
            .eq(user_id > 0, EventOrder.user_id, user_id) \
            .eq(param.status is not None, EventOrder.status, param.status) \
            .eq(param.base_coin is not None, EventOrder.base_coin, param.base_coin) \
            .eq(param.intervals is not None, EventOrder.intervals, param.intervals) \
            .order_by(True, EventOrder.create_time, ascending=False) \
            .page(page=param.page_num, page_size=param.page_size)
