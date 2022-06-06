from datetime import datetime

from data.symbol import Symbol
from data.time_series import TimeSeries, DFTimeSeries
from query.forex import ForexAPIProvider

import yfinance as yf


class YFinanceForexAPIProvider(ForexAPIProvider):
    def get_daily_exchange_rates(self, date_begin: datetime, date_end: datetime, from_symbol: Symbol,
                                 to_symbol: Symbol) -> TimeSeries:
        joint_symbol = Symbol(f'{from_symbol.name}{to_symbol.name}=X')

        df = yf.download(tickers=joint_symbol, start=date_begin, end=date_end, interval='1d')

        df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Adj Close': 'adj_close',
                           'Volume': 'volume'})

        return DFTimeSeries(df[['open', 'close', 'low', 'high', 'adf_close']], date_begin, date_end, joint_symbol)
