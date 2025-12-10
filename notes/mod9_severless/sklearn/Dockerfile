# public image when working with AWS Lambda
FROM public.ecr.aws/lambda/python:3.13
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY pyproject.toml uv.lock ./

# for global installation of dependencies
RUN uv pip install --system -r <(uv export --format requirements-txt)

# copy the model to the container
COPY model.bin .
COPY lambda_function.py .

CMD ["lambda_function.lambda_handler"]
