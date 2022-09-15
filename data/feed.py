from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime

from data.symbol import Symbol
from data.topic import Topic


@dataclass_json
@dataclass
class Feed:
    @dataclass_json
    @dataclass
    class FeedTopic:
        topic: Topic
        relevance_score: float

    @dataclass_json
    @dataclass
    class FeedSymbol:
        symbol: Symbol
        relevance_score: float
        sentiment_score: float

    title: str
    url: str
    time_published: datetime
    authors: list[str]
    summary: str
    banner_image_url: str
    source: str
    category_within_source: str
    source_domain: str
    topics: list[FeedTopic]
    overall_sentiment_score: float
    symbol_sentiment: list[FeedSymbol]


@dataclass_json
@dataclass
class Feeds:
    feeds: list[Feed]