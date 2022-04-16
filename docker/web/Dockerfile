FROM python:3.9-slim

RUN apt -y update && apt -y upgrade
RUN apt -y install \
    # Necessary for pip install
    gcc g++ libc-dev \
    # For psycopg2 (postgresql client)
    libpq-dev \
    # For development and debug
    bash vim \
    # For scikit-learn (scipy)
    gfortran libopenblas-dev liblapack-dev \
    # For opencv-python
    libopencv-dev \
    # libgl1-mesa-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

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
