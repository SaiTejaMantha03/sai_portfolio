#!/usr/bin/env python
"""
Database setup and migration script for deployment
This ensures all tables are created and data is populated
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.conf import settings

def check_database():
    """Check database connection and tables"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"📊 Found {len(tables)} tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def run_migrations():
    """Force run all migrations"""
    print("🗄️ Running migrations...")
    
    # Reset migrations (only if needed)
    try:
        execute_from_command_line(['manage.py', 'migrate', '--fake-initial'])
        print("✅ Fake initial migration completed")
    except:
        pass
    
    # Run all migrations
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("✅ All migrations completed")

def populate_data():
    """Populate database with initial data"""
    print("📊 Populating database...")
    try:
        # Import and run the populate script
        from populate_db import populate_database
        populate_database()
        print("✅ Database populated successfully")
    except Exception as e:
        print(f"⚠️ Data population failed: {e}")

def main():
    print("🚀 Starting database setup...")
    print(f"📍 Database: {settings.DATABASES['default']['ENGINE']}")
    print(f"📍 Database file: {settings.DATABASES['default'].get('NAME', 'N/A')}")
    
    # Check current state
    if not check_database():
        print("❌ Database connection failed")
        return
    
    # Run migrations
    run_migrations()
    
    # Check again after migrations
    check_database()
    
    # Populate data
    populate_data()
    
    print("🎉 Database setup complete!")

if __name__ == '__main__':
    main()