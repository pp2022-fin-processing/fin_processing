from query.provider import APIProvider
from query.yfinance.forex import YFinanceForexQueryAPIProvider
from query.yfinance.fundamental import YFinanceFundamentalQueryAPIProvider
from query.yfinance.stock import YFinanceStockQueryAPIProvider


class YFinanceAPIProvider(APIProvider):
    def fundamental(self):
        return YFinanceFundamentalQueryAPIProvider()

    def stock(self):
        return YFinanceStockQueryAPIProvider()

    def forex(self):
        return YFinanceForexQueryAPIProvider()

    def news_and_sentiments(self):
        pass
