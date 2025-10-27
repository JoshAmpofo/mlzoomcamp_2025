FROM python:3.12.12-slim-trixie

## recommended way to pip install uv on docker (from the uv team)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/ 

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY ".python-version" "pyproject.toml" "uv.lock" ./

# means install dependencies (exactly as in uv.lock) without updating them
RUN uv sync --locked 

COPY "workshop_predict.py" "workshop_model.bin" ./

EXPOSE 9696

ENTRYPOINT ["uvicorn", "workshop_predict:app", "--host", "0.0.0.0", "--port", "9696"]