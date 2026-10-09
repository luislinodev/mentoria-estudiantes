#!/bin/sh
set -e

echo "Preparando la base de datos local..."
python manage.py migrate --noinput

exec "$@"
