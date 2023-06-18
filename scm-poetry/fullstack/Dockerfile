# syntax=docker/dockerfile:1

FROM python:3.10.11-slim
WORKDIR /app
ENV PYTHONPATH /app
RUN mkdir /app/.streamlit /app/pages
COPY .env /app
COPY .streamlit/secrets.toml /app/.streamlit
COPY message_counts.csv /app
COPY pyproject.toml /app
COPY slackbolt_csv.py /app
COPY pages /app
COPY start.sh /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
ENTRYPOINT ["sh", "/app/start.sh"]
