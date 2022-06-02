import math
from dataclasses import dataclass
from decimal import Decimal

import requests
from datetime import time, timedelta, timezone, datetime
from abc import ABC, abstractmethod
from currencies import Currency
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

from data.data_point import DataPoint
from data.market import Market, Region
from data.symbol import Symbol
from data.symbol_type import SymbolType


@dataclass
class Interval:
    interval: timedelta

@dataclass
class MonthInterval(Interval):
    pass

@dataclass
class StockDataQuery:
    interval: Interval
    symbol: Symbol

@dataclass
class StockDataQueryResult:
    query: StockDataQuery
    results: list[DataPoint]

class StockAPI(ABC):
    @abstractmethod
    def supported_intervals(self) -> list[Interval]:
        pass

    @abstractmethod
    def make_query(self, query: StockDataQuery) -> StockDataQueryResult:
        pass


class AlphaVantageStockAPI(StockAPI):
    key: str
    __url: str = 'https://www.alphavantage.co/query'
    __daily: str = 'TIME_SERIES_DAILY'
    __apikey: str = 'apikey'

    def __init__(self, key: str):
        super().__init__()
        self.key = key

    def supported_intervals(self) -> list[Interval]:
        return [
            Interval(timedelta(minutes=1)),
            Interval(timedelta(minutes=5)),
            Interval(timedelta(minutes=15)),
            Interval(timedelta(minutes=30)),
            Interval(timedelta(minutes=60)),
            Interval(timedelta(days=1)),
            Interval(timedelta(weeks=1)),
            MonthInterval(timedelta(days=30)),
        ]

    def __make_query(self, **kwargs):
        query_url = f'{self.__url}'
        arguments = '&'.join([f'{k}={v}' for k, v in kwargs.items()])
        return f'{query_url}?{arguments}&{self.__apikey}={self.key}'

    def __make_intraday_query(self, query: StockDataQuery) -> StockDataQueryResult:
        pass

    def __make_daily_query(self, query: StockDataQuery) -> StockDataQueryResult:
        query_url = self.__make_query(function=self.__daily, symbol=query.symbol.symbol)
        unprocessed_query_results = requests.get(query_url)
        data_json = unprocessed_query_results.json()
        datetime_format = '%Y-%m-%d'
        time_series_processed = [
            DataPoint(
                datetime.strptime(k, datetime_format),
                query.interval.interval,
                Decimal(v['1. open']),
                Decimal(v['2. high']),
                Decimal(v['3. low']),
                Decimal(v['4. close']),
                Decimal(v['5. volume'])
            )
            for k, v in data_json['Time Series (Daily)'].items()
        ]
        return StockDataQueryResult(query, time_series_processed)

    def __make_weekly_query(self, query: StockDataQuery) -> StockDataQueryResult:
        pass

    def __make_monthly_query(self, query: StockDataQuery) -> StockDataQueryResult:
        pass

    def make_query(self, query: StockDataQuery) -> StockDataQueryResult:
        if query.interval.interval < timedelta(days=1):
            return self.__make_intraday_query(query)
        elif query.interval.interval == timedelta(days=1):
            return self.__make_daily_query(query)
        elif query.interval.interval == timedelta(weeks=1):
            return self.__make_weekly_query(query)
        elif query.interval.interval == timedelta(days=30):
            return self.__make_monthly_query(query)
        else:
            return None


def common_entries(*dcts):
    if not dcts:
        return
    for i in set(dcts[0]).intersection(*dcts[1:]):
        yield (i,) + tuple(d[i] for d in dcts)


def main():
    key = 'PUW1OQME6VCHNZE8'
    api = AlphaVantageStockAPI(key=key)
    results_ibm = api.make_query(
        StockDataQuery(
            Interval(timedelta(days=1)),
            Symbol('IBM', None, None, None)
        )
    )

    results_apple = api.make_query(
        StockDataQuery(
            Interval(timedelta(days=1)),
            Symbol('AAPL', None, None, None)
        )
    )

    results_ibm_mapping = {v.datetime_stamp: v for v in results_ibm.results}
    results_apple_mapping = {v.datetime_stamp: v for v in results_apple.results}

    common = list(common_entries(results_ibm_mapping, results_apple_mapping))
    common = list(sorted(common))

    ibm_sorted = [float(v_ibm.open_price) for k, v_ibm, v_apple in common]
    apple_sorted = [float(v_apple.open_price) for k, v_ibm, v_apple in common]

    ibm_apple = np.array([
        ibm_sorted,
        apple_sorted
    ])

    ibm_mean = np.mean(ibm_sorted)
    apple_mean = np.mean(apple_sorted)

    ibm_apple_cov = np.cov(ibm_apple)

    ibm_var = ibm_apple_cov[0][0]
    apple_var = ibm_apple_cov[1][1]

    ibm_sigma = math.sqrt(ibm_var)
    apple_sigma = math.sqrt(apple_var)

    ibm_x = np.linspace(ibm_mean - 3 * ibm_sigma, ibm_mean + 3 * ibm_sigma, 100)
    apple_x = np.linspace(apple_mean - 3 * apple_sigma, apple_mean + 3 * apple_sigma, 100)

    plt.plot(ibm_x, stats.norm.pdf(ibm_x, ibm_mean, ibm_sigma))
    plt.plot(apple_x, stats.norm.pdf(apple_x, apple_mean, apple_sigma))
    plt.show()

    beta_ibm = ibm_apple_cov[0][1] / ibm_var
    beta_apple = ibm_apple_cov[0][1] / apple_var

    print(beta_ibm)
    print(beta_apple)
    return
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=gazprom&apikey={key}'
    r = requests.get(url)
    data = r.json()

    #for match in data['bestMatches']:
    #    print(match)
    #return

    interval = '1min'
    datetime_format = '%Y-%m-%d %H:%M:%S'
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=300135.SHZ&apikey={key}'
    r = requests.get(url)
    data = r.json()
    print(data.keys())
    print(data)
    metadata = data['Meta Data']
    datetime_series = data[f'Time Series Crypto ({interval})']
    datetime_points = sorted(datetime_series.keys())

    time_points = list(map(lambda tp: datetime.strptime(tp, datetime_format).time(), datetime_points))
    time_series = {tp: datetime_series[dtp] for tp, dtp in zip(time_points, datetime_points)}

    symbol = metadata['2. Digital Currency Code']
    date = datetime.strptime(metadata['6. Last Refreshed'], datetime_format).date()

    print(f'Symbol: {symbol} at {date}')

    xdata = [tp.strftime("%H:%M:%S") for tp in time_points]
    ydata = [avg_data(time_series[tp]) for tp in time_points]
    #for time_point in time_points:
    #    print(f'Data at {time_point}: {time_series[time_point]}')
    #print(f'Time Series: {time_series}')
    #print(data.keys())
    print(xdata)
    plt.plot(xdata, ydata)
    plt.show()

if __name__ == '__main__':
    main()
