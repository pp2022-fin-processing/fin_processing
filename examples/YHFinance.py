import requests

from secrets.SecretsProvider import SecretProvider

url = "https://yh-finance.p.rapidapi.com/auto-complete"
querystring = {"q": "tesla", "region": "US"}
secret_provider = SecretProvider()
key = secret_provider.get_api_credentials('rapid_api')['api_key']


headers = {
    "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
    "X-RapidAPI-Key": key
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
