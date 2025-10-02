#!/bin/bash

# Deployment preparation script
echo "🚀 Preparing for deployment..."

# Run migrations
echo "📋 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional - comment out for automated deployment)
# echo "👤 Creating superuser..."
# python manage.py createsuperuser --noinput

echo "✅ Deployment preparation complete!"