from twelvedata import TDClient

from secrets.SecretsProvider import SecretProvider


def on_event(e):
    # do whatever is needed with data
    print(e)


secret_provider = SecretProvider()
api_key = secret_provider.get_api_credentials('twelve_data')['api_key']
td = TDClient(apikey=api_key)
ws = td.websocket(symbols="BTC/USD", on_event=on_event)
ws.subscribe(['ETH/BTC', 'AAPL'])
ws.connect()
ws.keep_alive()
