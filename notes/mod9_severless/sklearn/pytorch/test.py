import requests

# url = "http://localhost:8080/2015-03-31/functions/function/invocations"

url = "https://5kql2bfngd.execute-api.eu-west-1.amazonaws.com/classify-test/classify"

request = {
    "url": "http://bit.ly/mlbookcamp-pants"
}

results = requests.post(url, json=request).json()
print(results)