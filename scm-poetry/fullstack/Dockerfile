# syntax=docker/dockerfile:1

FROM python:3.10.12-slim
WORKDIR /app
ENV PYTHONPATH /app
ENV MESSAGE_COUNTS_PATH=/app/data/message_counts.csv

RUN mkdir /app/.streamlit
RUN mkdir /app/pages

# Copy files to the appropriate paths in the container
COPY .env /app
COPY pyproject.toml /app
COPY slackbolt_csv.py /app
COPY pages/1_home.py /app/pages
COPY start.sh /app

# Install Poetry and project dependencies
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Expose the necessary port(s) for your Streamlit application
EXPOSE 8501

# Set the entrypoint to start the application
ENTRYPOINT ["sh", "/app/start.sh"]
