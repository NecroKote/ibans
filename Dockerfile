FROM python:3.9.7-alpine

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.10

# create user with group and install poetry
RUN addgroup -g 1500 sven  \
    && adduser -D -G sven -u 1500 sven \
    && apk add --no-cache curl gcc libressl-dev musl-dev libffi-dev \
    && pip install "poetry==$POETRY_VERSION" \
    && apk del curl gcc libressl-dev musl-dev libffi-dev

# poetry dependencies install
WORKDIR /app
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

EXPOSE 8000
CMD ["hypercorn", "--access-logfile", "-", "-b", "0.0.0.0:8000", "ibans.asgi:app"]
USER sven

# actual code copying
COPY --chown=sven:sven ./ibans /app/ibans
USER sven