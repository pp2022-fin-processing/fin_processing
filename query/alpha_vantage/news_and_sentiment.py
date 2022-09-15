from dataclasses import dataclass
from datetime import datetime
from typing import Sequence, Optional
from urllib.parse import urlencode

import requests

from data.feed import Feed, Feeds
from data.symbol import Symbol
from data.topic import Topic
from query.news_and_sentiment import NewsAndSentimentQueryAPIProvider





@dataclass
class AlphaVantageNewsAndSentimentsAPIProvider(NewsAndSentimentQueryAPIProvider):
    api_key_v: str
    base_url: str = 'https://www.alphavantage.co/query?'

    @staticmethod
    def _decode_single_topic(json_obj: dict) -> Feed.FeedTopic:
        return Feed.FeedTopic(
            json_obj['topic'],
            float(json_obj['relevance_score'])
        )

    @staticmethod
    def _decode_single_symbol(json_obj: dict) -> Feed.FeedSymbol:
        return Feed.FeedSymbol(
            Symbol(json_obj['ticker']),
            float(json_obj['relevance_score']),
            float(json_obj['ticker_sentiment_score'])
        )

    @staticmethod
    def _decode_single_feed(json_obj: dict) -> Feed:
        return Feed(
            json_obj['title'],
            json_obj['url'],
            datetime.strptime(json_obj['time_published'], '%Y%m%dT%H%M%S'),
            json_obj['authors'],
            json_obj['summary'],
            json_obj['banner_image'],
            json_obj['source'],
            json_obj['category_within_source'],
            json_obj['source_domain'],
            [AlphaVantageNewsAndSentimentsAPIProvider._decode_single_topic(obj) for obj in json_obj['topics']],
            json_obj['overall_sentiment_score'],
            [AlphaVantageNewsAndSentimentsAPIProvider._decode_single_symbol(obj) for obj in json_obj['ticker_sentiment']]
        )

    def get_news_and_sentiment(self, symbols: Optional[Sequence[Symbol]] = None,
                               topics: Optional[Sequence[Topic]] = None,
                               date_start: Optional[datetime] = None, date_end: Optional[datetime] = None,
                               limit: Optional[int] = 50, sort: Optional[str] = 'LATEST') -> Feeds:
        function_v = 'NEWS_SENTIMENT'
        tickers_v = None if not symbols else ','.join([s.name for s in symbols])
        topics_v = None if not topics else ','.join([t.name for t in topics])
        time_from_v = None if not date_start else date_start.strftime('%Y%m%dT%H%M')
        time_to_v = None if not date_end else date_end.strftime('%Y%m%dT%H%M')
        sort_v = None if not sort else sort
        limit_v = None if not limit else str(limit)

        query_params = {
            'function': function_v,
            'apikey': self.api_key_v
        }

        if tickers_v:
            query_params['tickers'] = tickers_v
        if topics_v:
            query_params['topics'] = topics_v
        if time_from_v:
            query_params['time_from'] = time_from_v
        if time_to_v:
            query_params['time_to'] = time_to_v
        if sort_v:
            query_params['sort'] = sort_v
        if limit_v:
            query_params['limit'] = limit_v

        query_url = f'{self.base_url}{urlencode(query_params)}'

        response = dict(requests.get(query_url).json())
        return Feeds([AlphaVantageNewsAndSentimentsAPIProvider._decode_single_feed(obj) for obj in response['feed']])
