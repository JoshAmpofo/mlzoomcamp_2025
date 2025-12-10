#!/usr/bin/env python3


import boto3
import json

lambda_client = boto3.client('lambda')

customer = {
        "customer" : {
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

response = lambda_client.invoke(
        FunctionName='churn-prediction-docker',
        InvocationType='RequestResponse',
        Payload=json.dumps(customer)
    )

result = json.loads(response['Payload'].read())
print(json.dumps(result, indent=2))
