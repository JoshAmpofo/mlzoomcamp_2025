import numpy as np
import onnxruntime as ort
from keras_image_helper import create_preprocessor


import os
import pickle
from fastapi import FastAPI
import uvicorn

from typing import Literal
from pydantic import BaseModel, Field

model_name = os.getenv("MODEL_NAME", "clothing_classifier_mobilenet_v2_latest.onnx")


app = FastAPI(title='clothing-classifier-model')


def preprocess_pytorch_style(X):
    # X: shape (1, 299, 299, 3), dtype=float32, values in [0, 255]
    X = X / 255.0

    mean = np.array([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(1, 3, 1, 1)

    # Convert NHWC → NCHW
    # from (batch, height, width, channels) → (batch, channels, height, width)
    X = X.transpose(0, 3, 1, 2)  

    # Normalize
    X = (X - mean) / std

    return X.astype(np.float32)


preprocessor = create_preprocessor(
    preprocess_pytorch_style,
    target_size=(224, 224)
)

onnx_model_path = model_name
session = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

inputs = session.get_inputs()
input_name = inputs[0].name

outputs = session.get_outputs()
output_name = outputs[0].name

classes = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirt",
    "shoes",
    "shorts",
    "skirt",
    "t-shirt"
    ]

class PredictionResponse(BaseModel):
    predictions: dict[str, float]
    top_class: str
    top_probability: float


def predict_single(url: str) -> PredictionResponse:
    """Run inference on a single image URL and return class->probability mapping."""
    X = preprocessor.from_url(url)
    session_run = session.run([output_name], {input_name: X})
    float_preds = session_run[0][0].tolist()
    top_class = classes[float_preds.index(max(float_preds))]
    top_probability = max(float_preds)
    return PredictionResponse(
        predictions=dict(zip(classes, float_preds)),
        top_class=top_class,
        top_probability=top_probability
    )

def lambda_handler(event, context):
    url = event['url']
    return predict(url)


class Request(BaseModel):
    url: str = Field(..., description="URL of the image to classify", example="http://bit.ly/mlbookcamp-pants")


@app.post("/predict")
def predict(request: Request) -> PredictionResponse:
    return predict_single(request.url)


@app.get("/health")
def health():
    return {"status": "healthy"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)