# syntax=docker/dockerfile:1

FROM python:3.10.13-slim-bookworm
WORKDIR /app
ENV PYTHONPATH /app

COPY .env .
COPY . .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 3000

ENTRYPOINT ["sh", "/app/start_bolt.sh"]
