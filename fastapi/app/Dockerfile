# use alpine linux
FROM postgres:alpine

# current working directory
WORKDIR /code

# copy requirements only first
COPY ./requirements.txt /code/requirements.txt

# install package dependencies exclude cache
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy app dir inside code dir
COPY ./app /code/app

# placeholder to run stuff
# CMD [""]
