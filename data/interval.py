from dataclasses import dataclass
from enum import Enum


class IntervalPeriod(Enum):
    minutes = 0
    hours = 1
    days = 2
    weeks = 3
    months = 4


@dataclass
class Interval:
    period: IntervalPeriod
    count: int

    def __str__(self):
        if self.period == IntervalPeriod.minutes:
            return f'{self.count}m'
        elif self.period == IntervalPeriod.hours:
            return f'{self.count}h'
        elif self.period == IntervalPeriod.days:
            return f'{self.count}d'
        elif self.period == IntervalPeriod.weeks:
            return f'{self.count}w'
        elif self.period == IntervalPeriod.months:
            return f'{self.count}mth'
        else:
            return f'Unknown Period: {self.period}!'
