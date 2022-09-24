import dataclasses
from datetime import datetime, timedelta, date
from typing import Sequence

import numpy as np
import pandas
import pandas as pd

from data.feed import Feed, Feeds
from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from data.time_series import DFTimePoints, TimePoints
from query.alpha_vantage.provider import AlphaVantageAPIProvider
from os.path import exists

from query.yfinance.provider import YFinanceAPIProvider


def get_news_and_sentiments_for(date_start: datetime, date_end: datetime, symbol: Symbol):
    date_start_name = date_start.strftime('%d%m%Y')
    date_end_name = date_end.strftime('%d%m%Y')

    cache_name = f'{symbol.name}-{date_start_name}-{date_end_name}.json'

    if exists(cache_name):
        with open(cache_name, 'r') as f:
            nas_data = Feeds.from_json(f.read())
    else:
        provider = AlphaVantageAPIProvider()
        nas_provider = provider.news_and_sentiments()
        nas_data = nas_provider.get_news_and_sentiment(date_start=date_start, date_end=date_end,
                                                       symbols=[symbol])
        with open(cache_name, 'w') as f:
            f.write(nas_data.to_json())

    return nas_data


def get_stock_data(date_start: datetime, date_end: datetime, symbol: Symbol):
    date_start_name = date_start.strftime('%d%m%Y')
    date_end_name = date_end.strftime('%d%m%Y')

    cache_name = f'{symbol.name}-{date_start_name}-{date_end_name}.csv'

    if exists(cache_name):
        data = DFTimePoints(pd.read_csv(cache_name))
    else:
        provider = YFinanceAPIProvider()
        stock_provider = provider.stock()
        data = stock_provider.get_data(date_start, date_end, Interval(IntervalPeriod.days, 1), symbol, False)

        data.time_points().as_pandas_df().to_csv(cache_name)

    return data


def get_relevant_data(feed: Feed, data: pandas.DataFrame, symbol: Symbol):
    time_published = feed.time_published
    symbol_sentiment = list(filter(lambda x: x.symbol.name == symbol.name, feed.symbol_sentiment))[0]
    sentiment_score = symbol_sentiment.sentiment_score
    relevance_score = symbol_sentiment.relevance_score

    data_df = data.as_pandas_df()
    data_df["date"] = pd.to_datetime(data_df["date"]).dt.date
    evaluated_data = data_df[
        (data_df["date"] > (time_published - timedelta(days=5)).date()) &
        (data_df["date"] < (time_published + timedelta(days=1)).date())
        ]
    reference_data = data_df[
        (data_df["date"] > (time_published - timedelta(days=7)).date()) &
        (data_df["date"] < (time_published + timedelta(days=3)).date())
    ]

    return evaluated_data, reference_data, sentiment_score, relevance_score, time_published


def max_diff_percentage(data_eval: pandas.DataFrame, data_ref: pandas.DataFrame, field: str):
    df_eval = data_eval[field].values.reshape((1, -1))
    df_ref = data_ref[field].values.reshape((-1, 1))
    mat_s = (df_eval - df_ref) / df_ref
    res_pos = np.argmax(mat_s, 0)
    res_neg = np.argmin(mat_s, 0)
    max_diff_pos = np.take_along_axis(mat_s, res_pos[None,:], 0)
    max_diff_neg = np.take_along_axis(mat_s, res_neg[None,:], 0)
    return np.concatenate((max_diff_pos[0], max_diff_neg[0]))

def evaluate_data(data_eval: pandas.DataFrame, data_ref: pandas.DataFrame):
    o_max_diff = max_diff_percentage(data_eval, data_ref, 'open')
    c_max_diff = max_diff_percentage(data_eval, data_ref, 'close')
    ac_max_diff = max_diff_percentage(data_eval, data_ref, 'adj_close')
    v_max_diff = max_diff_percentage(data_eval, data_ref, 'volume')

    return \
        o_max_diff[np.argmax(np.abs(o_max_diff))], c_max_diff[np.argmax(np.abs(c_max_diff))],\
        ac_max_diff[np.argmax(np.abs(ac_max_diff))], v_max_diff[np.argmax(np.abs(v_max_diff))],


def evaluate_feed(feed: Feed, data: pandas.DataFrame, symbol: Symbol):
    deval, dref, ss, rs, tp = get_relevant_data(feed, data, symbol)
    if abs(ss) < 0.1:
        return
    od, cd, acd, vd = evaluate_data(deval, dref)
    print(f'Feed = {feed.title}')
    print(f'\t SS = {ss}')
    print(f'\t RS = {rs}')
    print(f'\t OD = {od}, CD = {cd}, ACD = {acd}, VD = {vd}')
    avgd = (od + cd + acd)/3
    print(f'\t AVG(OD, CD, ACD) = {avgd}')
    print(f'\t RS*SS = {rs*ss}')
    credibility = -abs(1 - avgd/(rs*ss)) + 1
    print(f'\t credibility = {credibility}')


def main():
    date_begin = datetime.strptime("01/01/2022", '%d/%m/%Y')
    date_end = datetime.strptime("01/06/2022", '%d/%m/%Y')
    symbol = Symbol('AAPL')

    feeds = get_news_and_sentiments_for(date_begin, date_end, symbol)
    data = get_stock_data(date_begin - timedelta(days=5), date_end + timedelta(days=5), symbol)

    for feed in feeds.feeds:
        evaluate_feed(feed, data, symbol)

if __name__ == '__main__':
    main()
