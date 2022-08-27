from abc import ABC, abstractmethod

import pandas

from data.symbol import Symbol


class FundamentalQueryAPIProvider(ABC):
    @abstractmethod
    def get_dividends(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    @abstractmethod
    def get_splits(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    @abstractmethod
    def get_balance_sheet(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    @abstractmethod
    def get_cashflow(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    @abstractmethod
    def get_earnings(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    @abstractmethod
    def get_quarterly_earnings(self, symbol: Symbol) -> pandas.DataFrame:
        pass
