import abc
import decimal


class QuotesService(abc.ABC):
    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def get_price(self, baseCoin: str) -> decimal.Decimal:
        pass

    @abc.abstractmethod
    async def exit(self):
        pass
