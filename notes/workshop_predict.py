
import pickle
import uvicorn
from fastapi import FastAPI
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

# request
class Customer(BaseModel):
    gender: Literal["male", "female"]
    seniorcitizen: Literal[0, 1]
    partner: Literal["yes", "no"]
    dependents: Literal["yes", "no"]
    phoneservice: Literal["yes", "no"]
    multiplelines: Literal["yes", "no", "no_phone_service"]
    internetservice: Literal["dsl", "fiber_optic", "no"]
    onlinesecurity: Literal["yes", "no", "no_internet_service"]
    onlinebackup: Literal["yes", "no", "no_internet_service"]
    deviceprotection: Literal["yes", "no", "no_internet_service"]
    techsupport: Literal["yes", "no", "no_internet_service"]
    streamingtv: Literal["yes", "no", "no_internet_service"]
    streamingmovies: Literal["yes", "no", "no_internet_service"]
    contract: Literal["month-to-month", "one_year", "two_year"]
    paperlessbilling: Literal["yes", "no"]
    paymentmethod: Literal[
        "electronic_check", 
        "mailed_check", 
        "bank_transfer_(automatic)", 
        "credit_card_(automatic)"
        ]
    tenure: int = Field(..., ge=0)
    monthlycharges: float = Field(..., ge=0)
    totalcharges: float = Field(..., ge=0)

# response
class PredictionResponse(BaseModel):
    churn_probability: float
    churn: bool

app = FastAPI(title='churn-prediction')

input_file = 'workshop_model.bin'

# open input file
with open(input_file, 'rb') as file:
    pipeline = pickle.load(file)


def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


@app.post('/predict')
def predict(customer: Customer) -> PredictionResponse:
    prob = predict_single(customer.dict())
    
    return PredictionResponse(
        churn_probability=prob,
        churn=bool(prob >= 0.5)
    )
    
    
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9696)
