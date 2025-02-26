# start docker with python
FROM python:3.13.2-slim-bullseye



#setup linux with python
ENV PYTHONUNBUFFERED = 1



# update linux kernal & setup tools
RUN apt-get update && apt-get -y install gcc libpq-dev


# add folder project
WORKDIR /app


# copy requirements.txt at docker
COPY requirements.txt /app/requirements.txt


# install requirements.txt
RUN pip install -r /app/requirements.txt


# copy project folder
COPY . /app/