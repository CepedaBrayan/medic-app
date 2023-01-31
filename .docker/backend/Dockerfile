 FROM python:3.8.0

ENV PYTHONUNBUFFERED 1 

WORKDIR /app
ADD requirements.txt /app/


RUN \
    apt-get update && \
    apt-get clean

RUN pip install -r requirements.txt --no-cache-dir



 