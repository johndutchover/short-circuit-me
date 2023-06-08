# bolt/Dockerfile

FROM python:3.10.11-slim

WORKDIR /bolt
COPY .env /bolt
COPY pyproject.toml /bolt
COPY slackbolt_app.py /bolt
COPY message_counts.csv /bolt

ENV PYTHONPATH /bolt:${PYTHONPATH}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

HEALTHCHECK CMD curl --fail http://localhost:3000/_stcore/health

EXPOSE 3000
ENTRYPOINT ["python", "slackbolt_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
