#!/bin/bash

# Azure Web App Startup Command
# This file should be set as the startup command in Azure Web App Configuration

# Set Python path
export PYTHONPATH="${PYTHONPATH}:/home/site/wwwroot"

# Run database migrations on startup
python manage.py migrate --noinput

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 3 --timeout 600 portfolio_project.wsgi:application