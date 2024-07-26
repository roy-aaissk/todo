FROM python:3.11-slim

ENV PYTHONUNBUFFRED 1
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD exec gunicorn --bind :8080 --log-level=info --workers 3 --threads 3 --timeout 0 main:app
