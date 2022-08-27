from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, Tuple

from data.symbol import Symbol
from data.topic import Topic


@dataclass
class Feed:

    @dataclass
    class FeedTopic:
        topic: Topic
        relevance_score: float

    @dataclass
    class FeedSymbol:
        symbol: Symbol
        relevance_score: float
        sentiment_score: float

    title: str
    url: str
    time_published: datetime
    authors: Sequence[str]
    summary: str
    banner_image_url: str
    source: str
    category_within_source: str
    source_domain: str
    topics: Sequence[FeedTopic]
    overall_sentiment_score: float
    symbol_sentiment: Sequence[FeedSymbol]
