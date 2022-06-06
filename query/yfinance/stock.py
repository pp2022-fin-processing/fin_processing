from datetime import datetime

from data.symbol import Symbol
from data.time_series import TimeSeries, DFTimeSeries

import yfinance as yf

from query.stock import StockAPIProvider


class YFinanceStockAPIProvider(StockAPIProvider):
    def get_daily_data(self, date_begin: datetime, date_end: datetime, symbol: Symbol) -> TimeSeries:
        df = yf.download(tickers=symbol.name, start=date_begin, end=date_end, interval='1d')

        df = df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
                           'Volume': 'volume'})
        df.index.names = ['date']

        return DFTimeSeries(df[['open', 'close', 'low', 'high', 'adj_close', 'volume']], date_begin, date_end, symbol)
