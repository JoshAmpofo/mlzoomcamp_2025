FROM public.ecr.aws/lambda/python:3.13

RUN pip install onnxruntime keras-image-helper

# Copy function code
COPY lambda_function_onnx.py .
COPY clothing_classifier_mobilenet_v2_latest.onnx .

CMD ["lambda_function_onnx.lambda_handler"]