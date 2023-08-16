FROM python:3.11.4-bullseye

WORKDIR /app

RUN pip install poetry==1.5.1
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install
