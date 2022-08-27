from datetime import datetime

import numpy as np

from data.interval import Interval, IntervalPeriod
from symbols import indices, index_components, non_index_components
from query.yfinance.provider import YFinanceAPIProvider


def beta_coefficent(a, index):
    cov = np.cov(a, index)[0, 1]
    var = np.var(index)
    beta = cov / var
    return beta


def main():
    date_begin = datetime.strptime("01/01/2017", '%d/%m/%Y')
    date_end = datetime.strptime("06/06/2022", '%d/%m/%Y')

    provider = YFinanceAPIProvider()

    stock_provider = provider.stock()

    ind = dict()
    stc = dict()

    for name, symbol in indices.items():
        series = stock_provider.get_data(date_begin, date_end, Interval(IntervalPeriod.days, 1), symbol)
        ind[name] = series

    for name, symbol in index_components.items():
        series = stock_provider.get_data(date_begin, date_end,Interval(IntervalPeriod.days, 1), symbol)
        stc[name] = series

    for name, symbol in non_index_components.items():
        series = stock_provider.get_data(date_begin, date_end,Interval(IntervalPeriod.days, 1), symbol)
        stc[name] = series

    print(f'Market measures across [{date_begin.strftime("%d.%m.%Y")}] - [{date_end.strftime("%d.%m.%Y")}] time period:')

    for ind_name, index in ind.items():
        index_df = index.time_points().as_pandas_df()

        start_value = float(index_df.iloc[[0]]['close'])
        end_value = float(index_df.iloc[[-1]]['close'])
        mean = np.mean(index_df['close'])
        std = np.std(index_df['close'])

        print()
        print(f'Capitalization of [{ind_name}] at begin = {start_value}, at end = {end_value}')
        print(f'Percentage ROI from [{ind_name}] = {end_value / start_value * 100.0}%')
        print(f'Mean, std of [{ind_name}] = {mean}, {std}')

    for stc_name, a in stc.items():
        a_df = a.time_points().as_pandas_df()

        start_value = float(a_df.iloc[[0]]['close'])
        end_value = float(a_df.iloc[[-1]]['close'])
        mean = np.mean(a_df['close'])
        std = np.std(a_df['close'])

        print()
        print(f'Capitalization of [{stc_name}] at begin = {start_value}, at end = {end_value}')
        print(f'Percentage ROI from [{stc_name}] = {(end_value - start_value) / start_value * 100.0}%')
        print(f'Mean, std of [{stc_name}] = {mean}, {std}')

        for ind_name, index in ind.items():
            index_df = index.time_points().as_pandas_df()
            index_index = list(index_df.index)
            a_index = list(a_df.index)

            index_df = index_df[index_df.index.isin(a_index)]
            a_df = a_df.loc[a_df.index.isin(index_index)]

            beta_v = beta_coefficent(a_df['close'], index_df['close'])
            corr_v = np.corrcoef(a_df['close'], index_df['close'])[0, 1]
            print(f'Beta of [{stc_name}] against [{ind_name}] = {beta_v}')
            print(f'Correlation between [{stc_name}] and [{ind_name}] = {corr_v}')


if __name__ == '__main__':
    main()
