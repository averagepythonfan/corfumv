FROM tf_dota_pred_lab:latest

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .
COPY corfumv/ corfumv/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root
