FROM python:3.11-slim-buster
LABEL maintainer="ronmarti18@gmail.com"

RUN pip install poetry openai
RUN pip install flask_cors

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
RUN mkdir /code/static
WORKDIR /code
COPY . /code/

RUN poetry config virtualenvs.create false
RUN poetry install
