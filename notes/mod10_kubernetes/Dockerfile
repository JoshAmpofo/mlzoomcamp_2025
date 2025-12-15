FROM python:3.12-slim-bookworm

## recommended way to pip install uv on docker (from the uv team)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY ".python-version" "pyproject.toml" "uv.lock" ./


RUN uv sync 

COPY "app.py" "clothing_classifier_mobilenet_v2_latest.onnx" ./

EXPOSE 8080

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]