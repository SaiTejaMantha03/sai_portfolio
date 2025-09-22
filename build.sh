#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🚀 Starting Render deployment build..."

echo "📦 Installing requirements..."
pip install -r requirements.txt

echo "� Database diagnostics..."
echo "Current working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Environment variables:"
printenv | grep -E "(DATABASE|DB)" || echo "No database environment variables found"

echo "🗄️ Database setup - Creating all migrations..."
python manage.py makemigrations --noinput

echo "🗄️ Database setup - Making specific app migrations..."
python manage.py makemigrations apps --noinput || echo "Apps migrations already exist"
python manage.py makemigrations blog --noinput || echo "Blog migrations already exist"
python manage.py makemigrations projects --noinput || echo "Projects migrations already exist"

echo "🗄️ Database setup - Applying all migrations with verbose output..."
python manage.py migrate --noinput --verbosity=2

echo "🔍 Checking database tables..."
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
tables = cursor.fetchall()
print(f'Found {len(tables)} tables:')
for table in tables:
    print(f'  - {table[0]}')
"

echo "📋 Collecting static files..."
python manage.py collectstatic --noinput

echo "📊 Setting up database with comprehensive script..."
python setup_database.py

echo "🔧 Running database repair command..."
python manage.py fix_database

echo "✅ Build completed successfully!"bash
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