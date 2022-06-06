from dataclasses import dataclass

from query.csv_cache.forex import CachedForexAPIProvider
from query.csv_cache.indices import CachedIndicesAPIProvider
from query.csv_cache.stock import CachedStockAPIProvider
from query.provider import APIProvider


@dataclass
class CachedAPIProvider(APIProvider):
    api_provider: APIProvider
    cache_root: str = 'storage/csv/'

    def stock(self):
        return CachedStockAPIProvider(self.api_provider.stock(), self.cache_location)

    def forex(self):
        return CachedForexAPIProvider(self.api_provider.forex(), self.cache_location)

    def indices(self):
        return CachedIndicesAPIProvider(self.api_provider.indices(), self.cache_location)