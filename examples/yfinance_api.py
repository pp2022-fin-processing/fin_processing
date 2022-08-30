import yfinance as yf
import plotly.graph_objs as go


def get_yfinance(ticker, start_date, end_date, interval):
    return yf.download(tickers=ticker, start=start_date, end=end_date, interval='1d')


def get_shares_outstanding(ticker):
    return yf.Ticker(ticker).shares


def save_to_file(data, file):
    data.to_csv(file)


def plot_chart(data, currency):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name='market data'))
    fig.update_layout(
        title=currency + ' price evolution',
        yaxis_title=currency.rpartition('-')[0] + ' price (in ' + currency.rpartition('-')[2] + ")")
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=15, label="15m", step="minute", stepmode="backward"),
                dict(count=45, label="45m", step="minute", stepmode="backward"),
                dict(count=1, label="HTD", step="hour", stepmode="todate"),
                dict(count=6, label="6h", step="hour", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()


currencies = {
    "BTC-USD": "BTC-USD",
    "EUR-USD": "EURUSD=X",
    "USD-JPY": "JPY=X",
    "GBP-USD": "GBPUSD=X",
    "AUD-USD": "AUDUSD=X",
    "EUR-GBP": "EURGBP=X",
    "EUR-CHF": "EURCHF=X",
    "EUR-JPY": "EURJPY=X",
    "EUR-PLN": "EURPLN=X",
    "PLN-USD": "PLNUSD=X"
    # "snp": "^GSPC"
}
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
it_companies_shares_outstanding_path = 'data/earnings/IT-shares-outstanding'

start_date = "2017-01-01"
end_date = "2022-06-03"
interval = "1d"

for name in it_companies:
    # data = get_yfinance(currencies[name], start_date, end_date, interval)
    # print(data)
    # save_to_file(data, "data/currencies/" + name + ".csv")
    # plot_chart(data, name)
    data = get_shares_outstanding(it_companies[name])
    save_to_file(data, it_companies_shares_outstanding_path + "/" + name + ".csv")
