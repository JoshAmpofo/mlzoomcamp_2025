#!/usr/bin/env python3

import pickle
import requests

url = "http://0.0.0.0:9696/predict"
prod_url = "https://delicate-sun-2838.fly.dev/predict"

client = {
    "lead_source": "organic_search",
    "number_of_courses_viewed": 4,
    "annual_income": 80304.0
}

result = requests.post(prod_url, json=client).json()
print(f"Response: {result}")