FROM python:3.9-alpine

RUN apk add --no-cache \
    # Necessary for pip install
    gcc libc-dev \
    # For psycopg2 (postgresql client)
    postgresql-dev \
    # For development and debug
    bash vim

EXPOSE 8000

# for updating python module
RUN pip install --upgrade pip \
    && pip install pipenv

ARG workdir="opt"
WORKDIR /${workdir}
