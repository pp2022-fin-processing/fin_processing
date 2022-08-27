import json
from datetime import datetime

from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from query.yfinance.provider import YFinanceAPIProvider
from query.provider import APIProvider
import matplotlib.pyplot as plt

def main():
    f = open("../../vault.json", 'r')
    data = json.load(f)
    f.close()

    provider: APIProvider = YFinanceAPIProvider()

    forex = provider.forex()
    fundamental = provider.fundamental()

    date_begin = datetime.strptime("01/01/2000", '%d/%m/%Y')
    date_end = datetime.strptime("17/08/2022", '%d/%m/%Y')

    #data = forex.get_exchange_rates(date_begin, date_end, Interval(IntervalPeriod.days, 1), Symbol('USD'), Symbol('PLN'))
    #data_to_plot = (data.time_points().open() + data.time_points().close())/2
    data_fundamental = fundamental.get_dividends(Symbol("AMZN"))
    print(data_fundamental)
    #plt.plot(data_fundamental)
    #plt.show()


if __name__ == '__main__':
    main()
