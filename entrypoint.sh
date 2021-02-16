#!/bin/sh
python manage.py makemigrations 2>&1;
python manage.py migrate 2>&1;
python manage.py collectstatic --no-input
python manage.py loaddata fixtures.json
gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
exec "$@"