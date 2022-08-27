from data.symbol import Symbol
from query.alpha_vantage.provider import AlphaVantageAPIProvider
import json

def main():
    provider = AlphaVantageAPIProvider('E8AV2HTOX7YMASMG')
    nas_provider = provider.news_and_sentiment()

    nas_data = nas_provider.get_news_and_sentiment(symbols=[Symbol('AAPL')])
    json_object = json.dumps(nas_data, indent=2)
    print(json_object)


if __name__ == '__main__':
    main()
