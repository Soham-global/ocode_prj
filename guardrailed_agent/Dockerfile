FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml ./

RUN uv pip install --system \
    fastapi==0.115.0 \
    "uvicorn[standard]==0.30.6" \
    pydantic==2.9.2 \
    langgraph==0.2.34 \
    langchain-core==0.3.10 \
    langchain-groq==0.2.0 \
    python-dotenv==1.0.1 \
    httpx==0.27.2

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
