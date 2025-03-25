import abc
import decimal

from bytoken.org.common.utils.ResultPage import ResultPage
from bytoken.org.model.EventOrder import OrderParam, EventOrder


class EventOrderService(abc.ABC):
    @abc.abstractmethod
    def post_order(self, user_id: int, order: OrderParam):
        pass

    @abc.abstractmethod
    def close_orders(self, coin: str, price: decimal.Decimal):
        pass

    @abc.abstractmethod
    def order_pages(self, user_id: int, param: OrderParam) -> ResultPage[EventOrder]:
        pass
