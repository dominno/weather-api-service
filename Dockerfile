FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY scripts/setup_localstack.py /app/setup_localstack.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
