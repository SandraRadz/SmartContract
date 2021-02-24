FROM python:3.7.3

LABEL maintainer="kundik.kirill@gmail.com"
LABEL version="0.0.1"
LABEL description="Image for Uni project"
LABEL url="https://escrow.university-search.online"

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/
