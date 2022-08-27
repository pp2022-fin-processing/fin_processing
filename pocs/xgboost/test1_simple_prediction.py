from datetime import datetime

import numpy as np
from sklearn.metrics import mean_squared_error

from xgboost import XGBRegressor, plot_importance

from data.interval import Interval, IntervalPeriod
from data.symbol import Symbol
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize
from query.provider import APIProvider
from query.yfinance.provider import YFinanceAPIProvider
import matplotlib.pyplot as plt


def create_model(**params):
    return XGBRegressor(
        objective='reg:squarederror',
        **params
    )


def forecast(trainX, trainY, testX, model):
    model.fit(trainX, trainY)

    resultY = model.predict(testX)

    return resultY


def prepare_provider() -> APIProvider:
    return YFinanceAPIProvider()


def create_features(df, label=None):
    df['date'] = df.index.values.astype(np.int64)/1e15
    df['dayofweek'] = df.index.dayofweek
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day

    outX = df[
        ['date', 'month', 'year', 'dayofweek', 'dayofyear', 'dayofmonth']
    ]

    if label:
        outY = df[label]
        return outX, outY

    return outX


def split(df, date_split):
    return df.loc[df.index < date_split], df.loc[df.index >= date_split]


def get_data(date_begin, date_end, date_split, symbol1, symbol2=None):
    api_provider = prepare_provider()
    forex = api_provider.forex()
    stock = api_provider.stock()

    symbol_from = symbol1
    symbol_to = symbol2

    if symbol_to:
        data = forex.get_exchange_rates(date_begin, date_end, Interval(IntervalPeriod.days, 1),
                                        symbol_from, symbol_to).time_points().as_pandas_df()
    else:
        data = stock.get_data(date_begin, date_end, Interval(IntervalPeriod.days, 1),
                              symbol_from, False).time_points().as_pandas_df()

    return split(data, date_split)


def optimization_space():
    return [
        Integer(1, 5, name='max_depth'),
        Integer(15, 100, name='n_estimators'),
        Real(10**-5, 10**0, 'log-uniform', name='learning_rate'),
        Real(10 ** -5, 10 ** 1, 'log-uniform', name='reg_alpha'),
        Real(10 ** -5, 10 ** 1, 'log-uniform', name='reg_lambda'),
    ]


def evaluate_model(realY, predictedY):
    return mean_squared_error(realY, predictedY)


def main():
    date_begin = datetime.strptime("01/01/2014", '%d/%m/%Y')
    date_end = datetime.strptime("01/01/2016", '%d/%m/%Y')

    date_split = datetime.strptime("01/09/2015", '%d/%m/%Y')

    symbol_from = Symbol("AAPL")
    symbol_to = None#Symbol("PLN")
    data_train, data_test = get_data(date_begin, date_end, date_split, symbol_from, symbol_to)

    trainX, trainY = create_features(data_train, 'close')
    testX, testY = create_features(data_test, 'close')

    space = optimization_space()

    @use_named_args(space)
    def objective(**params):
        model = create_model(**params)
        resultY = forecast(trainX, trainY, testX, model)
        return evaluate_model(testY, resultY)

    optimization_result = gp_minimize(objective, space, n_calls=50, random_state=0)
    print(f'Best score: {optimization_result.fun}')
    best_params = {
        space[i].name: optimization_result.x[i] for i in range(len(optimization_result.x))
    }
    print(f'Best param values: {best_params}')

    model = create_model(**best_params)
    resultY = forecast(trainX, trainY, testX, model)

    plt.plot(trainX.index, trainY, label='Train')
    plt.plot(testX.index, resultY, label='Predicted')
    plt.plot(testX.index, testY, label='Actual')
    plt.legend()
    plt.title(symbol_from.name if not symbol_to else f'{symbol_from.name} -> {symbol_to.name}')
    plt.show()

    plot_importance(model, height=0.9)
    plt.show()

    pass


if __name__ == '__main__':
    main()
