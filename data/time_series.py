from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

import pandas

from data.symbol import Symbol


class TimePoints(ABC):
    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def open(self) -> pandas.DataFrame:
        pass

    @abstractmethod
    def close(self) -> pandas.DataFrame:
        pass

    @abstractmethod
    def high(self) -> pandas.DataFrame:
        pass

    @abstractmethod
    def low(self) -> pandas.DataFrame:
        pass

    @abstractmethod
    def adj_close(self) -> pandas.DataFrame:
        pass

    @abstractmethod
    def volume(self) -> pandas.DataFrame:
        pass

    @abstractmethod
    def as_pandas_df(self) -> pandas.DataFrame:
        pass


class TimeSeries(ABC):
    @abstractmethod
    def time_points(self) -> TimePoints:
        pass

    @abstractmethod
    def date_begin(self) -> datetime:
        pass

    @abstractmethod
    def date_end(self) -> datetime:
        pass

    @abstractmethod
    def symbol(self) -> Symbol:
        pass


@dataclass
class DFTimePoints(TimePoints):
    data: pandas.DataFrame

    def __len__(self) -> int:
        return len(self.data.index)

    def open(self) -> pandas.DataFrame:
        return self.data['open']

    def close(self) -> pandas.DataFrame:
        return self.data['close']

    def adj_close(self) -> pandas.DataFrame:
        return self.data['adj_close']

    def volume(self) -> pandas.DataFrame:
        return self.data['volume']

    def high(self) -> pandas.DataFrame:
        return self.data['high']

    def low(self) -> pandas.DataFrame:
        return self.data['low']

    def as_pandas_df(self) -> pandas.DataFrame:
        return self.data


@dataclass
class DFTimeSeries(TimeSeries):
    data: pandas.DataFrame
    _date_begin: datetime
    _date_end: datetime
    _symbol: Symbol

    def time_points(self) -> TimePoints:
        return DFTimePoints(self.data)

    def date_begin(self) -> datetime:
        return self._date_begin

    def date_end(self) -> datetime:
        return self._date_end

    def symbol(self) -> Symbol:
        return self._symbol

    def save_csv_daily(self, path: str) -> None:
        with open(path, 'w') as f:
            f.write(f'{self.symbol().name}\n')
            f.write(f'{self.date_begin().strftime("%Y-%m-%d")}\n')
            f.write(f'{self.date_end().strftime("%Y-%m-%d")}\n')
            f.write(self.data.to_csv())


    @staticmethod
    def load_csv_daily(path: str) -> DFTimeSeries:
        with open(path, 'r') as f:
            data = f.read().splitlines()
            symbol = Symbol(data[0])
            date_begin = datetime.strptime(data[1], "%Y-%m-%d")
            date_end = datetime.strptime(data[2], "%Y-%m-%d")
            data = pandas.read_csv('\n'.join(data[3:]))

            return DFTimeSeries(data, date_begin, date_end, symbol)
