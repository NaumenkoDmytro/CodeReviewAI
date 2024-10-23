FROM python:3.12.2

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml  ./

RUN poetry install --no-root

# CMD ["poetry", "run", "uvicorn", "app.main:app", "--reload"]