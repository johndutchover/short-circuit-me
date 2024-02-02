# syntax=docker/dockerfile:1
FROM python:3.10.13-slim-bookworm
WORKDIR /app
ENV PYTHONPATH /app

# Install apt-utils first to avoid debconf warning
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the necessary files from the repository root
COPY .env pyproject.toml poetry.lock /app/

# Install poetry and project dependencies, upgrade pip first
RUN pip install --upgrade pip \
    && pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the application-specific files from the backend subdirectory
COPY backend/slackbolt_api.py backend/start_bolt.sh /app/

EXPOSE 3000

ENTRYPOINT ["sh", "/app/start_bolt.sh"]
