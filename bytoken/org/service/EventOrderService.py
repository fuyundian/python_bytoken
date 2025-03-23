import abc

from bytoken.org.model.EventOrder import OrderParam


class EventOrderService(abc.ABC):
    @abc.abstractmethod
    def postOrder(self, user_id: int, order: OrderParam):
        pass
