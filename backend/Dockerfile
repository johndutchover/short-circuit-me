# syntax=docker/dockerfile:1
FROM python:3.10.13-slim-bookworm
WORKDIR /app
ENV PYTHONPATH /app

# Copy only the necessary files
COPY .env pyproject.toml poetry.lock ./

# Install poetry and project dependencies
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the remaining project files
COPY . .

EXPOSE 3000

ENTRYPOINT ["sh", "/app/start_bolt.sh"]
