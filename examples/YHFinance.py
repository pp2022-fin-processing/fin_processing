import requests

url = "https://yh-finance.p.rapidapi.com/auto-complete"
querystring = {"q": "tesla", "region": "US"}
key = "78da9ef6bemsh47cf5019622f249p1d6768jsn4649c36a3cc8"

headers = {
    "X-RapidAPI-Host": "yh-finance.p.rapidapi.com",
    "X-RapidAPI-Key": key
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
