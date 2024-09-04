#!/bin/sh

export FLASK_APP=app.py 
export FLASK_ENV=development  

echo "Waiting for the availability of the DB..."
while ! nc -z flask_db 5432; do
  sleep 1
done

echo "DB is up and running."

if [ ! -d "migrations" ]; then
  echo "No migrations folder found. Initializing migrations..."
  flask db init
fi

if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions)" ]; then
  echo "No migration scripts found. Creating initial migration..."
  flask db migrate -m "Initial migration"
else
  echo "Migration scripts found. Skipping migration creation."
fi

echo "Running database upgrade..."
flask db upgrade

if [ $? -ne 0 ]; then
  echo "Migration failed. Check for errors."
  exit 1
fi

echo "Starting Flask application..."
exec flask run --host=0.0.0.0 --port=4000