from dataclasses import dataclass
from datetime import datetime

from data.symbol import Symbol
from data.time_series import TimeSeries

from query.indices import IndicesAPIProvider


@dataclass
class CachedIndicesAPIProvider(IndicesAPIProvider):
    api_provider: IndicesAPIProvider
    cache_root: str = 'storage/csv/'

    def get_daily_data(self, date_begin: datetime, date_end: datetime, symbol: Symbol) -> TimeSeries:
        pass
