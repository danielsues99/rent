#!/bin/sh

# Waiting for DB
echo "Waiting for the availability of the DB..."
while ! nc -z flask_db 5432; do
  sleep 1
done

echo "DB is up and running. Running migrations..."

flask db upgrade

exec flask run --host=0.0.0.0 --port=4000
