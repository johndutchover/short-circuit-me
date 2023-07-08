# syntax=docker/dockerfile:1

FROM python:3.10.12-slim-bookworm
WORKDIR /app
ENV PYTHONPATH /app

RUN mkdir /app/.streamlit
RUN mkdir /app/pages

COPY .env /app
COPY .streamlit/secrets.toml /app/.streamlit
COPY . .
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 8501
ENTRYPOINT ["sh", "/app/start_streamlit.sh"]
