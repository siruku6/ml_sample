FROM python:3.9-alpine

RUN apk add --no-cache \
    # Necessary for pip install
    gcc g++ libc-dev \
    # For psycopg2 (postgresql client)
    postgresql-dev \
    # For development and debug
    bash vim \
    # For scikit-learn (scipy)
    gfortran openblas-dev lapack-dev

# for updating python module
RUN pip install --upgrade pip \
    && pip install pipenv

EXPOSE 8000
ARG workdir="opt"
WORKDIR /${workdir}

# Install pip modules
COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv lock -r --dev > requirements.txt \
    && pip install -r requirements.txt
