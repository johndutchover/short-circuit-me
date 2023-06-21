# syntax=docker/dockerfile:1

FROM python:3.10.12-slim AS builder

WORKDIR /app
ENV PYTHONPATH /app
ENV MESSAGE_COUNTS_PATH=/app/data/message_counts.csv

RUN mkdir /app/.streamlit
RUN mkdir /app/pages

# Copy files to the appropriate paths in the container
COPY .env pyproject.toml slackbolt_csv.py pages/1_app.py start.sh /app/

# Install Poetry and project dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# ---- Final image ----
FROM python:3.10.12-slim

WORKDIR /app
ENV PYTHONPATH /app
ENV MESSAGE_COUNTS_PATH=/app/data/message_counts.csv

# Copy files from the builder stage
COPY --from=builder /app /app

# Expose the necessary port(s) for your Streamlit application
EXPOSE 8501

# Set the entrypoint to start the application
ENTRYPOINT ["sh", "/app/start.sh"]
