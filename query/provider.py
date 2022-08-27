from abc import ABC, abstractmethod

from query.forex import ForexQueryAPIProvider
from query.fundamental import FundamentalQueryAPIProvider
from query.stock import StockQueryAPIProvider


class APIProvider(ABC):
    @abstractmethod
    def stock(self) -> StockQueryAPIProvider:
        pass

    @abstractmethod
    def forex(self) -> ForexQueryAPIProvider:
        pass

    @abstractmethod
    def fundamental(self) -> FundamentalQueryAPIProvider:
        pass
