FROM public.ecr.aws/lambda/python:3.13

RUN pip install onnxruntime keras-image-helper

# Copy function code
COPY lambda_function_onnx.py .
COPY clothing-model-new.onnx .

CMD ["lambda_function_onnx.lambda_handler"]