FROM python:3.10-slim-bookworm

RUN pip install google-cloud-bigquery kafka-python
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

CMD ["python", "main.py"]
