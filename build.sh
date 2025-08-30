#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing requirements..."
pip install -r requirements.txt

echo "Making migrations..."
python manage.py makemigrations --verbosity=2

echo "Running migrations..."
python manage.py migrate --verbosity=2

echo "Collecting static files..."
python manage.py collectstatic --no-input --verbosity=2

echo "Build completed successfully!"