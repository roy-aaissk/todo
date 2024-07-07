FROM python:3.11-slim

ENV PYTHONUNBUFFRED True
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8080

CMD exec gunicorn --bind :8080 --workers 3 --threads 3 --timeout 0 main:app
