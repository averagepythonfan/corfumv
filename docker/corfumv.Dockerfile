FROM python:3.10-slim

RUN python3 -m pip install "poetry==1.3.2"

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only dev

WORKDIR /app

COPY corfumv/ corfumv/