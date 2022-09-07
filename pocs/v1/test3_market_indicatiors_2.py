import statistics
import time
from datetime import datetime

from data.interval import IntervalPeriod, Interval
from pocs.v1.symbols import it_companies
from query.yfinance.fundamental import YFinanceFundamentalsStoredDataProvider
from query.yfinance.stock import YFinanceStockStoredDataProvider

CLOSE_COLUMN = 4


def main():
    date_begin = datetime.strptime("28/09/2021", '%d/%m/%Y')
    date_end = datetime.strptime("31/12/2021", '%d/%m/%Y')

    print(
        f'Market measures across [{date_begin.strftime("%d.%m.%Y")}] - [{date_end.strftime("%d.%m.%Y")}] time period:')

    fundamentals_provider = YFinanceFundamentalsStoredDataProvider()
    stock_provider = YFinanceStockStoredDataProvider()

    all_iter_times_data_collection = []
    all_iter_times_calculations = []
    iteration = 0
    while iteration < 100:
        times_data_collection = []
        times_calculations = []

        for name, symbol in it_companies.items():
            start_time = time.time_ns()

            stock = stock_provider.get_data(date_begin, date_end, Interval(IntervalPeriod.days, 1), symbol)
            earnings = fundamentals_provider.get_earnings(symbol, date_begin, date_end)
            shares_outstanding = fundamentals_provider.get_shares_outstanding(symbol, date_begin, date_end)
            time_after_data_collection = time.time_ns()

            eps = calculate_eps(earnings, shares_outstanding)
            pb = calculate_pb(stock, earnings, shares_outstanding)
            pe = calculate_pe(stock, earnings, shares_outstanding)
            # print(f'Ticker: {name}')
            # print(f'EPS: {eps}')
            # print(f'P/B: {pb}')
            # print(f'P/E: {pe}')
            time_after_calculations = time.time_ns()

            times_data_collection.append(time_after_data_collection - start_time)
            times_calculations.append(time_after_calculations - time_after_data_collection)

        # all_iter_times_data_collection.append(sum(times_data_collection))
        # all_iter_times_calculations.append(sum(times_calculations))
        all_iter_times_data_collection.append(statistics.mean(times_data_collection))
        all_iter_times_calculations.append(statistics.mean(times_calculations))

        print(f'Iteration {iteration}: Total data collection time:  {sum(times_data_collection) / 10e6}[ms]'
              f' | Total calculation time:  {sum(times_calculations) / 10e6}[ms]')
        iteration += 1

    print()
    print(f'Average data collection time: {statistics.mean(all_iter_times_data_collection) / 10e6}[ms]')
    print(f'Average calculation time: {statistics.mean(all_iter_times_calculations) / 10e6}[ms]')


def calculate_eps(earnings, shares_outstanding):
    return int(earnings['netIncome']) / shares_outstanding


def calculate_pb(stock, earnings, shares_outstanding):
    results = []
    for index, row in stock.iterrows():
        results.append(float(row[CLOSE_COLUMN]) / ((float(earnings['totalAssets']) - float(earnings['totalLiab']))
                                                   / float(shares_outstanding)))
    return results


def calculate_pe(stock, earnings, shares_outstanding):
    results = []
    for index, row in stock.iterrows():
        results.append(float(row[CLOSE_COLUMN]) / calculate_eps(earnings, shares_outstanding))


if __name__ == '__main__':
    main()
