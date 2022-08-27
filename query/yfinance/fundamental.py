from datetime import datetime
from typing import Sequence

import pandas

from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from data.time_series import TimeSeries, DFTimeSeries
from query.fundamental import FundamentalQueryAPIProvider

import yfinance as yf


class YFinanceFundamentalQueryAPIProvider(FundamentalQueryAPIProvider):
    def get_earnings(self, symbol: Symbol) -> pandas.DataFrame:
        return yf.Ticker(symbol.name).earnings

    def get_quarterly_earnings(self, symbol: Symbol) -> pandas.DataFrame:
        return yf.Ticker(symbol.name).quarterly_earnings

    def get_splits(self, symbol: Symbol) -> TimeSeries:
        return yf.Ticker(symbol.name).get_splits()

    def get_balance_sheet(self, symbol: Symbol) -> TimeSeries:
        return yf.Ticker(symbol.name).get_balance_sheet()

    def get_cashflow(self, symbol: Symbol) -> TimeSeries:
        return yf.Ticker(symbol.name).get_cashflow()

    def get_dividends(self, symbol: Symbol) -> TimeSeries:
        return yf.Ticker(symbol.name).get_dividends()
