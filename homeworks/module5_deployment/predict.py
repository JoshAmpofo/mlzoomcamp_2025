#!/usr/bin/env python3


import pickle
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from typing import Dict, Any, Literal


app = FastAPI(title="client-conversion")

model_file = "pipeline_v1.bin"

with open(model_file, "rb") as f_in:
    pipeline = pickle.load(f_in)

# request
class Client(BaseModel):
    lead_source: str
    number_of_courses_viewed: int
    annual_income: float

# response
class PredictResponse(BaseModel):
    probability: float
    convert: bool


def predict_single(client):
    result = pipeline.predict_proba([client])[0, 1]
    return float(result)


@app.post('/predict')
def predict(client: Client) -> PredictResponse:
    probability = predict_single(client.dict())

    return PredictResponse(
        probability=probability,
        convert=bool(probability >= 0.5)
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)