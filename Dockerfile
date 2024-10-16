FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y cron

EXPOSE 5000
EXPOSE 8501

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
