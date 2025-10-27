import requests

url = "http://localhost:9696/predict"
prod_url = "https://nameless-morning-7231.fly.dev/predict"

customer = {
    "gender": "male",
    "seniorcitizen": 1,
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
    "tenure": 45,
    "monthlycharges": 104.2,
    "totalcharges": (45 * 104.2)
}

response = requests.post(prod_url, json=customer).json()
print(f"Response: {response}")

if response['churn'] >= 0.5:
    print('Sending promotional email to customer')
else:
    print('No promotional email needed')