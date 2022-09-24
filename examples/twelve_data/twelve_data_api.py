import pandas as pd
import requests

from secrets.SecretsProvider import SecretProvider

secret_provider = SecretProvider()
api_key = secret_provider.get_api_credentials('twelve_data')['api_key']
ticker = "MSFT"
interval = "1day"
api_url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval={interval}&apikey={api_key}"

json = requests.get(api_url).json()
data = pd.DataFrame(json["values"])
print(data)
