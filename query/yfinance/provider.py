from query.provider import APIProvider
from query.yfinance.forex import YFinanceForexAPIProvider
from query.yfinance.indices import YFinanceIndicesAPIProvider
from query.yfinance.stock import YFinanceStockAPIProvider


class YFinanceAPIProvider(APIProvider):
    def stock(self):
        return YFinanceStockAPIProvider()

    def forex(self):
        return YFinanceForexAPIProvider()

    def indices(self):
        return YFinanceIndicesAPIProvider()