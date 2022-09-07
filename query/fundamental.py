from abc import ABC, abstractmethod
from datetime import datetime

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
    def get_earnings(self, symbol: Symbol, date_start: datetime, date_end: datetime) -> dict:
        pass

    @abstractmethod
    def get_quarterly_earnings(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    @abstractmethod
    def get_shares_outstanding(self, symbol: Symbol, date_start: datetime, date_end: datetime) -> int:
        pass
