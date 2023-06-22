# syntax=docker/dockerfile:1

FROM python:3.10.12-slim
WORKDIR /app
ENV PYTHONPATH /app
ENV MESSAGE_COUNTS_PATH=/app/data/message_counts.csv

COPY .env .
COPY . .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 3000

ENTRYPOINT ["sh", "/app/start_bolt.sh"]
