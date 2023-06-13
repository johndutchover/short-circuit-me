# syntax=docker/dockerfile:1

FROM python:3.10.11-slim
WORKDIR /bolt
ENV PYTHONPATH /bolt:${PYTHONPATH}
COPY .env /bolt
COPY pyproject.toml /bolt
COPY slackbolt_csv.py /bolt
# COPY message_counts.csv /bolt
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 3000
ENTRYPOINT ["python", "slackbolt_csv.py", "--server.port=3000", "--server.address=0.0.0.0"]
