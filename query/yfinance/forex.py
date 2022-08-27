from datetime import datetime
from typing import Sequence

from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from data.time_series import TimeSeries, DFTimeSeries
from query.forex import ForexQueryAPIProvider

import yfinance as yf


class YFinanceForexQueryAPIProvider(ForexQueryAPIProvider):
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
    def _get_data(date_start: datetime, date_end: datetime, symbol: Symbol, interval: str) -> TimeSeries:
        df = yf.download(tickers=symbol.name, start=date_start, end=date_end, interval=interval)

        df = df.rename(
            columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
                     'Volume': 'volume'})
        df.index.names = ['date']

        return DFTimeSeries(df[['open', 'close', 'low', 'high', 'adj_close', 'volume']], date_start, date_end, symbol)

    def get_exchange_rates(self, date_start: datetime, date_end: datetime, interval: Interval, from_symbol: Symbol,
                           to_symbol: Symbol) -> TimeSeries:
        symbol = Symbol(f'{from_symbol.name}{to_symbol.name}=X')

        if interval == Interval(IntervalPeriod.days, 1):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '1d')
        elif interval == Interval(IntervalPeriod.days, 5):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '5d')
        elif interval == Interval(IntervalPeriod.months, 1):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '1mo')
        elif interval == Interval(IntervalPeriod.months, 3):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '3mo')
        elif interval == Interval(IntervalPeriod.months, 6):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '6mo')
        elif interval == Interval(IntervalPeriod.months, 12):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '1y')
        elif interval == Interval(IntervalPeriod.months, 24):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '2y')
        elif interval == Interval(IntervalPeriod.months, 60):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '5y')
        elif interval == Interval(IntervalPeriod.months, 120):
            return YFinanceForexQueryAPIProvider._get_data(date_start, date_end, symbol, '10y')
        else:
            raise ValueError(f'Unsupported interval: {interval}')
