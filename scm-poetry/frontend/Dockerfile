# app/Dockerfile

FROM python:3.10.11-slim

WORKDIR /app

COPY pyproject.toml /app
COPY streamlit_app.py /app
COPY message_counts.csv /app

ENV PYTHONPATH /app:${PYTHONPATH}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
