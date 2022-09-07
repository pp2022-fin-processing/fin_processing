import os
from datetime import datetime

import pandas
import pandas as pd
import yfinance as yf
import csv

from data.symbol import Symbol
from data.time_series import TimeSeries
from query.fundamental import FundamentalQueryAPIProvider


class YFinanceFundamentalQueryAPIProvider(FundamentalQueryAPIProvider):
    def get_earnings(self, symbol: Symbol, date_start: datetime, date_end: datetime) -> pandas.DataFrame:
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

    def get_shares_outstanding(self, symbol: Symbol) -> pandas.DataFrame:
        return yf.Ticker(symbol.name).get_shares()


class YFinanceFundamentalsStoredDataProvider(FundamentalQueryAPIProvider):

    path_to_earnings = '../../examples/data/earnings/IT'
    path_to_shares_outstanding = '../../examples/data/earnings/IT-shares-outstanding'

    def get_dividends(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    def get_splits(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    def get_balance_sheet(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    def get_cashflow(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    def get_earnings(self, symbol: Symbol, date_start: datetime, date_end: datetime) -> dict:
        with open(f'{self.path_to_earnings}/{symbol.full_name}.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            result = dict()
            proper_column = -1
            for row in reader:
                if line_count == 0:
                    column = 1
                    while column < len(row):
                        column_date = datetime.strptime(row[column], '%Y-%m-%d')
                        if date_start < column_date < date_end:
                            proper_column = column
                        column += 1
                else:
                    property_name = row[0]
                    result[property_name] = row[proper_column]
                line_count += 1
            return result

    def get_quarterly_earnings(self, symbol: Symbol) -> pandas.DataFrame:
        pass

    def get_shares_outstanding(self, symbol: Symbol, date_start: datetime, date_end: datetime) -> int:
        with open(f'{self.path_to_shares_outstanding}/{symbol.full_name}.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            result = -1
            for row in reader:
                if line_count != 0:
                    column_date = datetime.strptime(row[0], '%Y')
                    if date_start.year == column_date.year:
                        result = int(row[1])
                line_count += 1
            return result
