from dataclasses import dataclass

from query.alpha_vantage.news_and_sentiment import AlphaVantageNewsAndSentimentsAPIProvider
from query.alpha_vantage.stock import AlphaVantageStockAPIProvider
from query.forex import ForexQueryAPIProvider
from query.fundamental import FundamentalQueryAPIProvider
from query.news_and_sentiment import NewsAndSentimentQueryAPIProvider
from query.provider import APIProvider
from query.stock import StockQueryAPIProvider


@dataclass
class AlphaVantageAPIProvider(APIProvider):
    api_key_v: str

    def stock(self) -> StockQueryAPIProvider:
        return AlphaVantageStockAPIProvider(self.api_key_v)

    def forex(self) -> ForexQueryAPIProvider:
        pass

    def fundamental(self) -> FundamentalQueryAPIProvider:
        pass

    def news_and_sentiments(self) -> NewsAndSentimentQueryAPIProvider:
        return AlphaVantageNewsAndSentimentsAPIProvider(self.api_key_v)
