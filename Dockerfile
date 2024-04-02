FROM python:3.12 AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


FROM python-base AS builder-base
RUN apt-get update \
 && apt-get install -y gcc git

WORKDIR $PYSETUP_PATH
COPY ./pyproject.toml ./poetry.lock ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir setuptools wheel \
 && pip install --no-cache-dir poetry

RUN poetry install --no-dev

FROM python-base AS production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
RUN apt-get update && apt-get install -y curl

WORKDIR .
COPY . .
CMD ["python", "-Om", "src"]