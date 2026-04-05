#!/bin/sh

set -e

echo "Starting application"

echo "Applying migrations"
python manage.py migrate --noinput

echo "Collect static"
python manage.py collectstatic --noinput

echo "App is ready!!!"

exec "$@"