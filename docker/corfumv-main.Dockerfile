FROM python:3.10-slim

RUN pip install poetry==1.7.1

COPY poetry.lock .
COPY pyproject.toml .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only dev

WORKDIR /app

COPY corfumv/ corfumv/

ENTRYPOINT [ "uvicorn", "corfumv.server:app", "--host=0.0.0.0", "--port=11000", "--reload" ]