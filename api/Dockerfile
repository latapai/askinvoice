# Use an official Python runtime as a parent image
FROM python:3.11.8-bullseye

RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

COPY . /src
WORKDIR /src

COPY requirements.txt .

RUN pip3 install -r requirements.txt


COPY . .

EXPOSE 8000

CMD uvicorn asset_api:app --reload --port 8000
