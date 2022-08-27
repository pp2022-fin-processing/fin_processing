from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from data.interval import Interval
from data.symbol import Symbol
from data.time_series import TimeSeries


class ForexQueryAPIProvider(ABC):
    @abstractmethod
    def available_intervals(self) -> Sequence[Interval]:
        pass

    @abstractmethod
    def get_exchange_rates(self, date_start: datetime, date_end: datetime, interval: Interval, from_symbol: Symbol,
                           to_symbol: Symbol) -> TimeSeries:
        pass
