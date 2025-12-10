import io
import urllib.request

import numpy as np
import onnxruntime as ort
from PIL import Image

# Model expects NCHW float32 normalized like ImageNet
onnx_model_path = "hair_classifier_empty.onnx"
session = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Preprocessing constants
INPUT_SIZE = 200
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def load_image_from_url(url: str) -> Image.Image:
    with urllib.request.urlopen(url) as resp:
        buf = resp.read()
    return Image.open(io.BytesIO(buf))


def preprocess_image(img: Image.Image) -> np.ndarray:
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((INPUT_SIZE, INPUT_SIZE), Image.NEAREST)
    arr = np.array(img).astype(np.float32) / 255.0  # HWC in [0,1]
    arr = (arr - MEAN) / STD                         # normalize
    arr = np.transpose(arr, (2, 0, 1))               # to CHW
    arr = np.expand_dims(arr, axis=0)                # add batch -> NCHW
    return arr


def predict_from_url(image_url: str):
    img = load_image_from_url(image_url)
    x = preprocess_image(img)
    result = session.run([output_name], {input_name: x})
    return result[0][0].tolist()


def lambda_handler(event, context):
    url = event["image_url"]
    prediction = predict_from_url(url)
    return {
        "statusCode": 200,
        "body": prediction,
    }