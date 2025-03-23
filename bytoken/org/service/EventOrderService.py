import abc
import decimal

from bytoken.org.model.EventOrder import OrderParam


class EventOrderService(abc.ABC):
    @abc.abstractmethod
    def postOrder(self, user_id: int, order: OrderParam):
        pass

    @abc.abstractmethod
    def closeOrders(self, coin: str, price: decimal.Decimal):
        pass
