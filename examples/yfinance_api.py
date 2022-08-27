import yfinance as yf
import plotly.graph_objs as go


def get_yfinance(ticker, start_date, end_date, interval):
    return yf.download(tickers=ticker, start=start_date, end=end_date, interval='1d')


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
    #"snp": "^GSPC"
}
start_date = "2017-01-01"
end_date = "2022-06-03"
interval = "1d"

for name in currencies:
    data = get_yfinance(currencies[name], start_date, end_date, interval)
    print(data)
    #save_to_file(data, "data/currencies/" + name + ".csv")
   # plot_chart(data, name)
