import onnxruntime as ort
from keras_image_helper import create_preprocessor

onnx_model_path = "clothing-model-new.onnx"
session = ort.InferenceSession(onnx_model_path, providers=["CPUExecutionProvider"])

inputs = session.get_inputs()
input_name = inputs[0].name  # onnxruntime uses singular `name`

outputs = session.get_outputs()
output_name = outputs[0].name


preprocessor = create_preprocessor('xception', target_size=(299, 299))

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


def predict_from_url(url: str) -> dict:
    """Run inference on a single image URL and return class->probability mapping."""
    X = preprocessor.from_url(url)
    session_run = session.run([output_name], {input_name: X})
    float_preds = session_run[0][0].tolist()
    return dict(zip(classes, float_preds))

def lambda_handler(event, context):
    url = event['url']
    return predict_from_url(url)