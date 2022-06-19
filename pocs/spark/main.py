import time

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean, stddev

from examples.yahoo_fin_api import it_companies
from examples.yfinance_api import currencies


def map_reduce_example():
    conf = SparkConf().setAppName("FinanceProcessing").setMaster("local")
    sc = SparkContext(conf=conf)

    lines = sc.textFile("../../examples/data/currencies/BTC-USD.csv")
    lines_numbers = lines.filter(lambda x: x.find("Date") == -1)

    single_values = lines_numbers.map(lambda x: x.split(","))
    adj_close = single_values.map(lambda x: x[4])

    result = adj_close.reduce(lambda x, y: float(x) + float(y))
    print(result)


def main():
    spark = SparkSession.builder.appName('Practise').getOrCreate()

    for currency in currencies:
        start_time = time.time()

        path = f'../../examples/data/currencies/{currency}.csv'
        df = spark.read.option('header', 'true').csv(path, inferSchema=True)

        start_value = df.head()[5]
        end_value = df.tail(1)[0]['Close']
        roi = (end_value - start_value) / start_value * 100.0

        print(currency)
        print(f"start value: {start_value}")
        print(f"End value: {end_value}")
        print(f"ROI: {roi}%")
        df_close = df.select(mean('Close'), stddev('Close'))
        df_close.show()

        end_time = time.time()
        print(f'Processing time: {end_time - start_time}s \n')

    for it_company in it_companies:
        start_time = time.time()

        path = f'../../examples/data/IT/{it_company}.csv'
        df = spark.read.option('header', 'true').csv(path, inferSchema=True)

        start_value = df.head()[3]
        end_value = df.tail(1)[0]['close']
        roi = (end_value - start_value) / start_value * 100.0

        print(it_company)
        print(f"start value: {start_value}")
        print(f"End value: {end_value}")
        print(f"ROI: {roi}%")
        df_close = df.select(mean('Close'), stddev('Close'))
        df_close.show()

        end_time = time.time()
        print(f'Processing time: {end_time - start_time}s \n')


if __name__ == '__main__':
    main()
