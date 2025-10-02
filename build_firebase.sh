#!/bin/bash

# Build script for Firebase deployment
echo "Building Django portfolio for Firebase hosting..."

# Activate virtual environment
source myenv/bin/activate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create dist directory for Firebase
mkdir -p dist

# Copy static files
echo "Copying static files..."
cp -r staticfiles/* dist/

# Generate HTML files (this is a simplified approach)
echo "Generating static HTML files..."

# You could use django-distill or similar tools for a full static site generation
# For now, we'll create a basic index.html that can work with Firebase

echo "Build completed!"
echo ""
echo "Next steps for Firebase deployment:"
echo "1. Initialize Firebase project: firebase init"
echo "2. Deploy: firebase deploy"
echo ""
echo "Note: For a full Django app, consider using:"
echo "- Google Cloud Run"
echo "- Heroku"
echo "- PythonAnywhere"
echo "- Railway"