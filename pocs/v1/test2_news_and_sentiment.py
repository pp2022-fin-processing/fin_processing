import dataclasses
from datetime import datetime

from data.symbol import Symbol
from query.alpha_vantage.provider import AlphaVantageAPIProvider
import json

def main():
    date_begin = datetime.strptime("01/01/2022", '%d/%m/%Y')
    date_end = datetime.strptime("01/06/2022", '%d/%m/%Y')

    provider = AlphaVantageAPIProvider('E8AV2HTOX7YMASMG')
    nas_provider = provider.news_and_sentiment()

    nas_data = nas_provider.get_news_and_sentiment(date_start=date_begin, date_end=date_end, symbols=[Symbol('AAPL')])
    json_object = json.dumps([dataclasses.asdict(feed) for feed in nas_data], indent=2, default=str)
    print(json_object)


if __name__ == '__main__':
    main()
