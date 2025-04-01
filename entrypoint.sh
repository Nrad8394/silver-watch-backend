#!/bin/sh

echo "cd into silver_watch..."
cd silver_watch

echo "Running makemigrations..."
python manage.py makemigrations --noinput

echo "Running migrate..."
python manage.py migrate --noinput

echo "Collecting Static Files..."
python manage.py collectstatic --noinput

echo "Starting Supervisor..."
exec supervisord -c /app/supervisord.conf
