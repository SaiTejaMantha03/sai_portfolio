#!/usr/bin/env python
"""
Quick database diagnostic script
Run this to check what database is being used
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from django.conf import settings

def main():
    print("🔍 Database Configuration Diagnostic")
    print("=" * 50)
    
    db_config = settings.DATABASES['default']
    
    print(f"Engine: {db_config['ENGINE']}")
    print(f"Name: {db_config.get('NAME', 'N/A')}")
    print(f"Host: {db_config.get('HOST', 'N/A')}")
    print(f"Port: {db_config.get('PORT', 'N/A')}")
    print(f"User: {db_config.get('USER', 'N/A')}")
    
    print("\n🔍 Environment Variables:")
    print(f"DATABASE_URL present: {'DATABASE_URL' in os.environ}")
    print(f"AZURE_SQL_SERVER present: {'AZURE_SQL_SERVER' in os.environ}")
    
    if 'DATABASE_URL' in os.environ:
        print(f"DATABASE_URL: {os.environ['DATABASE_URL'][:50]}...")
    
    print("\n🎯 Recommendation:")
    if db_config['ENGINE'] == 'django.db.backends.sqlite3':
        print("❌ Using SQLite - this will cause deployment issues on Render")
        print("✅ Solution: Add PostgreSQL DATABASE_URL environment variable")
    elif 'postgresql' in db_config['ENGINE']:
        print("✅ Using PostgreSQL - this should work correctly")
    elif 'sql_server' in db_config['ENGINE']:
        print("✅ Using SQL Server - configured for Azure")

if __name__ == '__main__':
    main()