#!/usr/bin/env bash
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py loaddata fixtures.json
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000