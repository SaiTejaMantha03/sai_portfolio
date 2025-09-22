#!/bin/bash

# Azure Web App Deployment Script
echo "🚀 Starting Azure Web App deployment build..."

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Import GitHub projects (if needed)
echo "📊 Importing GitHub projects..."
python manage.py import_github_projects || echo "⚠️ GitHub projects import failed or already exists"

# Create superuser (optional - only for first deployment)
# Uncomment the following lines if you want to create a superuser automatically
# echo "👤 Creating superuser (optional)..."
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'your-secure-password')" | python manage.py shell

echo "✅ Azure Web App deployment preparation complete!"
echo "🌐 Your app should be available at your Azure Web App URL"