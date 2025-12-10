import requests


customer = {
    "customer": {
        "gender": "female",
        "seniorcitizen": 0,
        "partner": "yes",
        "dependents": "yes",
        "phoneservice": "yes",
        "multiplelines": "yes",
        "internetservice": "fiber_optic",
        "onlinesecurity": "yes",
        "onlinebackup": "no",
        "deviceprotection": "yes",
        "techsupport": "no",
        "streamingtv": "yes",
        "streamingmovies": "yes",
        "contract": "month-to-month",
        "paperlessbilling": "yes",
        "paymentmethod": "electronic_check",
        "tenure": 17,
        "monthlycharges": 104.2,
        "totalcharges": 1743.5
        }
    }

#url = "http://localhost:8080/2015-03-31/functions/function/invocations"

url = "https://5tpq9q5w43.execute-api.eu-west-1.amazonaws.com/churn-test/predict"

result = requests.post(url, json=customer).json()
print(result)
