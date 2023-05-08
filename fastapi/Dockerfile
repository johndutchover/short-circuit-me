FROM python:3.10

# current working directory
WORKDIR /code

# copy requirements only first
COPY ./requirements.txt /code/requirements.txt

# install package dependencies exclude cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy app dir inside code dir
COPY ./app /code/app

# run uvicorn (from FastAPI quickstart) to verify
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
