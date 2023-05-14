FROM python:3.11

# current working directory
WORKDIR /code

# copy requirements only first
COPY requirements.txt /code

# install package dependencies exclude cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy app dir inside code dir
COPY ./app /code/app

# run uvicorn (from FastAPI quickstart) to verify
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "127.0.0.1", "--port", "8000"]
