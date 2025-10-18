#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Making migrations for all apps..."
python manage.py makemigrations apps
python manage.py makemigrations blog  
python manage.py makemigrations projects

echo "Running migrations..."
python manage.py migrate --run-syncdb

echo "Creating superuser..."
python manage.py create_superuser

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"