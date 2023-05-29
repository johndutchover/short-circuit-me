# bolt/Dockerfile

FROM python:3.10.11-slim

RUN mkdir /bolt
WORKDIR /bolt
COPY pyproject.toml /bolt
COPY slackbolt_app.py /bolt

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 3000
#HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
#ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
