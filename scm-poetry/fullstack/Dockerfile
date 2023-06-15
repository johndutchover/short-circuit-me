# syntax=docker/dockerfile:1

FROM python:3.10.11-slim
WORKDIR /app
ENV PYTHONPATH /app
# Create a directory for streamlit secrets
RUN mkdir /app/.streamlit
COPY .env /app
COPY .streamlit/secrets.toml /app/.streamlit
COPY message_counts.csv /app
COPY pyproject.toml /app
COPY slackbolt_full.py /app
COPY streamlit_app.py /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 8501
CMD ["python", "slackbolt_full.py"]
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
