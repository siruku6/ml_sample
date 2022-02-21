#!/bin/ash
# I use /bin/ash because in alpine container, we can't use bin/bash.

pipenv lock -r --dev > requirements.txt
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver 0.0.0.0:8000
