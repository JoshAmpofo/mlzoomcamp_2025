FROM agrigorev/model-2025-hairstyle:v1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY pyproject.toml uv.lock ./

RUN uv pip install --system -r <(uv export --format requirements-txt)

COPY lambda_function.py .

CMD ["lambda_function.lambda_handler"]