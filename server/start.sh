#!/bin/bash

# start.sh - Entrypoint script for Docker/Digital Ocean App Platform

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Applaude Server Setup..."

# 1. Wait for PostgreSQL database to be available (simple sleep, or use wait-for-it.sh)
echo "Waiting for database..."
sleep 5 

# 2. Run database migrations
echo "Running migrations..."
python manage.py migrate --noinput

# 3. Collect static files for serving (e.g., Django Admin static files)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 4. Start Gunicorn WSGI server in production mode
# Use the $PORT environment variable provided by the host (Digital Ocean)
echo "Starting Gunicorn WSGI server..."
exec gunicorn applaud.wsgi:application \
    --bind 0.0.0.0:"${PORT:-8000}" \
    --workers 4 \
    --timeout 120 \
    --log-level info
