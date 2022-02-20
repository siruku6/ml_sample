#!/bin/ash
# I use /bin/ash because in alpine container, we can't use bin/bash.

pipenv lock -r --dev > requirements.txt
pip install -r requirements.txt

python ml_sample/manage.py migrate
python ml_sample/manage.py runserver 0.0.0.0:8000
