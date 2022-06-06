from yahoo_fin.stock_info import get_data, get_earnings_in_date_range, get_financials


def get_yh_stocks(symbol, start_date, end_date, interval):
    return get_data(symbol, start_date=start_date, end_date=end_date, index_as_date=True, interval=interval)


def get_yh_earnings(symbol):
    return get_financials(symbol, False, True)


def save_to_file(data, file):
    data.to_csv(file)


def get_and_save_suite(path, suite):
    for name in suite:
        data = get_yh_stocks(suite[name], start_date, end_date, interval)
        save_to_file(data, f'{path}/{name}.csv')


it_companies = {
    "amazon": "amzn",
    "apple": "aapl",
    "google": "goog",
    "microsoft": "msft",
    "facebook": "ft",
    "adobe": "adbe",
    "accenture": "acn",
    "akamai": "akam",
    "activision": "atvi",
    "autodesk": "adsk",
    "nvidia": "nvda",
    "intel": "intc",
    "at&t": "t",
    "tmobile": "tmus"
}
it_companies_stock_path = 'data/shares/IT'
it_companies_earnings_path = 'data/earnings/IT'

indices = {
    "s&p": "^GSPC",
    "nasdaq": "^IXIC",
    "wig": "WIG"
}
indices_path = 'data/indices'
start_date = "01/01/2017"
end_date = "03/06/2022"
interval = "1d"

if __name__ == '__main__':
    print(get_yh_earnings('amzn'))

# get_and_save_suite(it_companies)
# get_and_save_suite(indices)
