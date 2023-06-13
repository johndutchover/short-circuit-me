# syntax=docker/dockerfile:1

FROM python:3.10.11-slim
WORKDIR /app
ENV PYTHONPATH /app:${PYTHONPATH}
COPY pyproject.toml /app
COPY streamlit_csv.py /app
#COPY message_counts.csv /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "streamlit_csv.py", "--server.port=8501", "--server.address=0.0.0.0"]
