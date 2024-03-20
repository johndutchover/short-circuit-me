# syntax=docker/dockerfile:1
FROM python:3.12-slim-bookworm
WORKDIR /app
ENV PIXI_VERSION=latest
ENV INSTALL_DIR=/usr/local/bin
ENV REPO=prefix-dev/pixi
ENV PLATFORM=unknown-linux-musl
ENV PROJECT_NAME=pixi-in-docker
ENV PYTHONPATH /app

# Install apt-utils first to avoid debconf warning
RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils curl tar \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download and install pixi
RUN if [ "$PIXI_VERSION" = "latest" ]; then \
      DOWNLOAD_URL="https://github.com/$REPO/releases/latest/download/pixi-$(uname -m)-$PLATFORM.tar.gz"; \
    else \
      DOWNLOAD_URL="https://github.com/$REPO/releases/download/$PIXI_VERSION/pixi-$(uname -m)-$PLATFORM.tar.gz"; \
    fi && \
    curl -SL "$DOWNLOAD_URL" | tar -xz -C "$INSTALL_DIR"

# Copy the necessary files from the repository root
COPY ../pixi.toml ../pixi.lock ../pyproject.toml backend/.env /app/

# Copy the application-specific files from the backend subdirectory
COPY backend/slackbolt_api.py backend/start_bolt.sh /app/

EXPOSE 3000

ENTRYPOINT ["pixi", "run", "-e", "prod", "start"]
