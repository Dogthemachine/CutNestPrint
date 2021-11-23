# Dockerfile
FROM python:3.7
ENV PYTHONUNBUFFERED 1
EXPOSE 8080
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install --upgrade pip
RUN apt update
RUN apt install gettext -y
RUN apt update
RUN apt upgrade -y
RUN apt install python3-opencv -y
RUN apt install build-essential python-dev libagg-dev libpotrace-dev pkg-config -y
RUN pip install -r requirements.txt