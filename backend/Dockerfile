From python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/backend
COPY huggingface_tasks/ /app/huggingface_tasks

CMD [ "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]