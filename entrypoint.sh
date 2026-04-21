#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate

echo "Creating default superuser..."
python manage.py create_default_superuser

echo "Starting gunicorn..."
exec gunicorn stripe_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2
