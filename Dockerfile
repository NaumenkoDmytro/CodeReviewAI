FROM python:3.10

RUN apt-get update && apt-get install -y curl 

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml  ./

RUN poetry install --no-root