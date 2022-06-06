from dataclasses import dataclass
from datetime import datetime

from data.symbol import Symbol
from data.time_series import TimeSeries
from query.forex import ForexAPIProvider


@dataclass
class CachedForexAPIProvider(ForexAPIProvider):
    api_provider: ForexAPIProvider
    cache_root: str = 'storage/csv/'

    def get_daily_exchange_rates(self, date_begin: datetime, date_end: datetime, from_symbol: Symbol,
                                 to_symbol: Symbol) -> TimeSeries:
        pass
