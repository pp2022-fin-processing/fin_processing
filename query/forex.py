from abc import ABC, abstractmethod
from datetime import datetime

from data.symbol import Symbol
from data.time_series import TimeSeries


class ForexAPIProvider(ABC):
    @abstractmethod
    def get_daily_exchange_rates(self, date_begin: datetime, date_end: datetime, from_symbol: Symbol,
                                 to_symbol: Symbol) -> TimeSeries:
        pass
