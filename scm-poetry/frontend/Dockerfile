# syntax=docker/dockerfile:1

FROM python:3.10.12-slim
WORKDIR /app
ENV PYTHONPATH /app
# Create a directory for streamlit secrets
RUN mkdir /app/.streamlit
COPY .env /app
COPY .streamlit/secrets.toml /app/.streamlit
COPY message_counts.csv /app
COPY pyproject.toml /app
COPY streamlit_app.py /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 8501
ENTRYPOINT ["sh", "/app/start_streamlit.sh"]
