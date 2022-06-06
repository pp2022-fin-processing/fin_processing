from abc import ABC, abstractmethod
from datetime import datetime

from data.symbol import Symbol
from data.time_series import TimeSeries


class StockAPIProvider(ABC):
    @abstractmethod
    def get_daily_data(self, date_begin: datetime, date_end: datetime, symbol: Symbol) -> TimeSeries:
        pass
