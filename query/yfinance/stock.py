import csv
from datetime import datetime
from typing import Sequence

import pandas as pd

from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from data.time_series import TimeSeries, DFTimeSeries

import yfinance as yf

from query.stock import StockQueryAPIProvider


class YFinanceStockQueryAPIProvider(StockQueryAPIProvider):
    def available_intervals(self) -> Sequence[Interval]:
        return [
            Interval(IntervalPeriod.days, 1),
            Interval(IntervalPeriod.days, 5),
            Interval(IntervalPeriod.months, 1),
            Interval(IntervalPeriod.months, 3),
            Interval(IntervalPeriod.months, 6),
            Interval(IntervalPeriod.months, 12),
            Interval(IntervalPeriod.months, 24),
            Interval(IntervalPeriod.months, 60),
            Interval(IntervalPeriod.months, 120),
        ]

    @staticmethod
    def _get_data(date_start: datetime, date_end: datetime, symbol: Symbol, interval: str, adjusted: bool = False) -> TimeSeries:
        df = yf.download(tickers=symbol.name, start=date_start, end=date_end, interval=interval, auto_adjust=adjusted)

        df = df.rename(
            columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
                     'Volume': 'volume'})
        df.index.names = ['date']

        return DFTimeSeries(df[['open', 'close', 'low', 'high', 'adj_close', 'volume']], date_start, date_end, symbol)

    def get_data(self, date_start: datetime, date_end: datetime, interval: Interval, symbol: Symbol,
                 adjusted: bool = False) -> TimeSeries:
        if interval == Interval(IntervalPeriod.days, 1):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '1d', adjusted)
        elif interval == Interval(IntervalPeriod.days, 5):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '5d', adjusted)
        elif interval == Interval(IntervalPeriod.months, 1):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '1mo', adjusted)
        elif interval == Interval(IntervalPeriod.months, 3):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '3mo', adjusted)
        elif interval == Interval(IntervalPeriod.months, 6):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '6mo', adjusted)
        elif interval == Interval(IntervalPeriod.months, 12):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '1y', adjusted)
        elif interval == Interval(IntervalPeriod.months, 24):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '2y', adjusted)
        elif interval == Interval(IntervalPeriod.months, 60):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '5y', adjusted)
        elif interval == Interval(IntervalPeriod.months, 120):
            return YFinanceStockQueryAPIProvider._get_data(date_start, date_end, symbol, '10y', adjusted)
        else:
            raise ValueError(f'Unsupported interval: {interval}')


class YFinanceStockStoredDataProvider(StockQueryAPIProvider):

    path_to_stock = '../../examples/data/shares/IT'

    def available_intervals(self) -> Sequence[Interval]:
        return [
            Interval(IntervalPeriod.days, 1),
        ]

    def get_data(self, date_start: datetime, date_end: datetime, interval: Interval, symbol: Symbol,
                 adjusted: bool = False):
        with open(f'{self.path_to_stock}/{symbol.full_name}.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            schema = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'adjclose': [],
                      'volume': [], 'ticker': []}
            data_frame = pd.DataFrame(schema)
            for row in reader:
                if line_count != 0:
                    row_date = datetime.strptime(row[0], '%Y-%m-%d')
                    if date_start < row_date < date_end:
                        new_row = pd.DataFrame({'date': [row[0]], 'open': [row[1]], 'high': [row[2]], 'low': [row[3]],
                                                'close': [row[4]], 'adjclose': [row[5]], 'volume': [row[6]], 'ticker': [row[7]]})
                        data_frame = pd.concat([data_frame, new_row])
                line_count += 1
            return data_frame
