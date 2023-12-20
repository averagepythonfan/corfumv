FROM python:3.10-slim

RUN pip install poetry==1.7.1

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --without test,client,build

WORKDIR /app

COPY corfumv/ corfumv/