from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from typing import Sequence
from urllib.parse import urlencode

import pandas as pd
import requests

from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from data.time_series import TimeSeries, DFTimeSeries
from query.stock import StockQueryAPIProvider


@dataclass
class AlphaVantageStockAPIProvider(StockQueryAPIProvider):
    api_key_v: str
    base_url: str = 'https://www.alphavantage.co/query?'
    intraday_function_v: str = 'TIME_SERIES_INTRADAY'
    intraday_extended_function_v: str = 'TIME_SERIES_INTRADAY_EXTENDED'
    daily_function_v: str = 'TIME_SERIES_DAILY'
    daily_adjusted_function_v: str = 'TIME_SERIES_DAILY_ADJUSTED'
    weekly_function_v: str = 'TIME_SERIES_WEEKLY'
    weekly_adjusted_function_v: str = 'TIME_SERIES_WEEKLY_ADJUSTED'
    monthly_function_v: str = 'TIME_SERIES_MONTHLY'
    monthly_adjusted_function_v: str = 'TIME_SERIES_MONTHLY_ADJUSTED'

    def available_intervals(self) -> Sequence[Interval]:
        return [
            Interval(IntervalPeriod.minutes, 1),
            Interval(IntervalPeriod.minutes, 5),
            Interval(IntervalPeriod.minutes, 15),
            Interval(IntervalPeriod.minutes, 30),
            Interval(IntervalPeriod.hours, 1),
            Interval(IntervalPeriod.days, 1),
            Interval(IntervalPeriod.weeks, 1),
            Interval(IntervalPeriod.months, 1),
        ]

    def convert_to_dataframe(self, response_csv: str) -> pd.DataFrame:
        df = pd.read_csv(StringIO(response_csv), index_col=0)
        df.index.names = ['date']
        df.index = pd.to_datetime(df.index)

        return df

    def get_intraday_data(self, date_start: datetime, date_end: datetime, symbol: Symbol, adjusted: bool,
                          interval_v: str) -> pd.DataFrame:
        function_v = self.intraday_extended_function_v
        symbol_v = symbol.name
        datatype_v = 'csv'
        adjusted_v = 'true' if adjusted else 'false'

        df = pd.DataFrame()

        for year_slice in range(1,3):
            for month_slice in range(1,13):
                slice_v = f'year{year_slice}month{month_slice}'

                query_params = {
                    'function': function_v,
                    'symbol': symbol_v,
                    'interval': interval_v,
                    'slice': slice_v,
                    'datatype': datatype_v,
                    'adjusted': adjusted_v,
                    'apikey': self.api_key_v
                }

                query_url = f'{self.base_url}{urlencode(query_params)}'

                response = requests.get(query_url)
                response_csv = response.content.decode('utf-8')

                next_df = self.convert_to_dataframe(response_csv)

                df = pd.concat([df, next_df])

        return df


    def get_daily_data(self, date_start: datetime, date_end: datetime, symbol: Symbol, adjusted: bool) -> pd.DataFrame:
        function_v = self.daily_adjusted_function_v if adjusted else self.daily_function_v
        symbol_v = symbol.name
        outputsize_v = 'full'
        datatype_v = 'csv'

        query_params = {
            'function': function_v,
            'symbol': symbol_v,
            'outputsize': outputsize_v,
            'datatype': datatype_v,
            'apikey': self.api_key_v
        }

        query_url = f'{self.base_url}{urlencode(query_params)}'

        response = requests.get(query_url)
        response_csv = response.content.decode('utf-8')

        df = self.convert_to_dataframe(response_csv)

        return df

    def get_weekly_data(self, date_start: datetime, date_end: datetime, symbol: Symbol, adjusted: bool) -> pd.DataFrame:
        function_v = self.weekly_adjusted_function_v if adjusted else self.weekly_function_v
        symbol_v = symbol.name
        datatype_v = 'csv'

        query_params = {
            'function': function_v,
            'symbol': symbol_v,
            'datatype': datatype_v,
            'apikey': self.api_key_v
        }

        query_url = f'{self.base_url}{urlencode(query_params)}'

        response = requests.get(query_url)
        response_csv = response.content.decode('utf-8')

        df = self.convert_to_dataframe(response_csv)

        return df

    def get_monthly_data(self, date_start: datetime, date_end: datetime, symbol: Symbol, adjusted: bool) -> pd.DataFrame:
        function_v = self.monthly_adjusted_function_v if adjusted else self.monthly_function_v
        symbol_v = symbol.name
        datatype_v = 'csv'

        query_params = {
            'function': function_v,
            'symbol': symbol_v,
            'datatype': datatype_v,
            'apikey': self.api_key_v
        }

        query_url = f'{self.base_url}{urlencode(query_params)}'

        response = requests.get(query_url)
        response_csv = response.content.decode('utf-8')

        df = self.convert_to_dataframe(response_csv)

        return df

    def get_data(self, date_start: datetime, date_end: datetime, interval: Interval, symbol: Symbol,
                 adjusted: bool = False) -> TimeSeries:
        if interval == Interval(IntervalPeriod.minutes, 1):
            df = self.get_intraday_data(date_start, date_end, symbol, adjusted, '1min')
        elif interval == Interval(IntervalPeriod.minutes, 5):
            df = self.get_intraday_data(date_start, date_end, symbol, adjusted, '5min')
        elif interval == Interval(IntervalPeriod.minutes, 15):
            df = self.get_intraday_data(date_start, date_end, symbol, adjusted, '15min')
        elif interval == Interval(IntervalPeriod.minutes, 30):
            df = self.get_intraday_data(date_start, date_end, symbol, adjusted, '30min')
        elif interval == Interval(IntervalPeriod.hours, 1):
            df = self.get_intraday_data(date_start, date_end, symbol, adjusted, '60min')
        elif interval == Interval(IntervalPeriod.days, 1):
            df = self.get_daily_data(date_start, date_end, symbol, adjusted)
        elif interval == Interval(IntervalPeriod.weeks, 1):
            df = self.get_weekly_data(date_start, date_end, symbol, adjusted)
        elif interval == Interval(IntervalPeriod.months, 1):
            df = self.get_monthly_data(date_start, date_end, symbol, adjusted)
        else:
            raise ValueError('!!!')

        df = df[(df.index >= date_start) & (df.index <= date_end)]

        return DFTimeSeries(df, date_start, date_end, symbol)

