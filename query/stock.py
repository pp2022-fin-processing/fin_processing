from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from data.interval import Interval
from data.symbol import Symbol
from data.time_series import TimeSeries


class StockQueryAPIProvider(ABC):
    @abstractmethod
    def available_intervals(self) -> Sequence[Interval]:
        pass

    @abstractmethod
    def get_data(self, date_start: datetime, date_end: datetime, interval: Interval, symbol: Symbol,
                 adjusted: bool = False) -> TimeSeries:
        pass
