from twelvedata import TDClient


def on_event(e):
    # do whatever is needed with data
    print(e)


td = TDClient(apikey="135c1aa9af6b4c41aa06955be5835abb")
ws = td.websocket(symbols="BTC/USD", on_event=on_event)
ws.subscribe(['ETH/BTC', 'AAPL'])
ws.connect()
ws.keep_alive()
