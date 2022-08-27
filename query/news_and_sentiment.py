from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence

from data.feed import Feed
from data.symbol import Symbol
from data.topic import Topic


class NewsAndSentimentQueryAPIProvider(ABC):
    @abstractmethod
    def get_news_and_sentiment(self, symbols: Optional[Sequence[Symbol]] = None,
                               topics: Optional[Sequence[Topic]] = None,
                               date_start: Optional[datetime] = None, date_end: Optional[datetime] = None,
                               limit: Optional[int] = 50, sort: Optional[str] = 'LATEST') -> Sequence[Feed]:
        pass
