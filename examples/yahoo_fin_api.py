from yahoo_fin.stock_info import get_data


def get_yahoo_fin(ticker, start_date, end_date, interval):
    return get_data(ticker, start_date=start_date, end_date=end_date, index_as_date=True, interval=interval)


def save_to_file(data, file):
    data.to_csv(file)


def get_and_save_suite(suite):
    for name in suite:
        data = get_yahoo_fin(suite[name], start_date, end_date, interval)
        save_to_file(data, "data/" + name + ".csv")


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
indices = {
    "s&p": "^GSPC",
    "nasdaq": "^IXIC",
    "wig": "WIG"
}
start_date = "01/01/2017"
end_date = "03/06/2022"
interval = "1d"

# get_and_save_suite(it_companies)
# get_and_save_suite(indices)
