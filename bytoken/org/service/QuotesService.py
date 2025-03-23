import abc
import decimal


class QuotesService(abc.ABC):
    @abc.abstractmethod
    async def init(self):
        pass

    @abc.abstractmethod
    def getPrice(self, baseCoin: str) -> decimal.Decimal:
        pass

    @abc.abstractmethod
    async def exit(self):
        pass
