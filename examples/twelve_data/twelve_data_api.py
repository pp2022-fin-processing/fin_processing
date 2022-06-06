import requests
import pandas as pd

api_key = "135c1aa9af6b4c41aa06955be5835abb"
ticker = "MSFT"
interval = "1day"
api_url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval={interval}&apikey={api_key}"

json = requests.get(api_url).json()
data = pd.DataFrame(json["values"])
print(data)
