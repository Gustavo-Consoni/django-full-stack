#!/bin/sh
set -e

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --clear --noinput

exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --threads 4
