FROM python:3.10-slim

RUN pip install poetry==1.7.1

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
COPY dist/ dist/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root
