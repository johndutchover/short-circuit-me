# app/Dockerfile

FROM python:3.10-slim

WORKDIR /app
COPY . /app
COPY pyproject.toml /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "short_circuit_me.py", "--server.port=8501", "--server.address=0.0.0.0"]