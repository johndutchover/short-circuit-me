# app/Dockerfile

FROM python:3.10.11-slim

RUN mkdir /app
WORKDIR /app
COPY pyproject.toml /app
COPY streamlit_app.py /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
