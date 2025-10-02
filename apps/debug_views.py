from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from django.core.management import call_command
import os
import io
import sys

def debug_database(request):
    """Debug endpoint to check database status and run migrations if needed"""
    
    html = "<h1>Database Debug Info</h1>"
    html += "<style>body { font-family: Arial; margin: 20px; } .success { color: green; } .error { color: red; } .warning { color: orange; }</style>"
    
    # Database configuration
    db_config = settings.DATABASES['default']
    html += f"<h2>Database Configuration</h2>"
    html += f"<p>Engine: {db_config['ENGINE']}</p>"
    html += f"<p>Name: {db_config.get('NAME', 'N/A')}</p>"
    html += f"<p>Host: {db_config.get('HOST', 'N/A')}</p>"
    html += f"<p>Port: {db_config.get('PORT', 'N/A')}</p>"
    
    # Environment variables
    html += f"<h2>Environment Variables</h2>"
    html += f"<p>DATABASE_URL present: {'DATABASE_URL' in os.environ}</p>"
    if 'DATABASE_URL' in os.environ:
        # Show partial URL for security
        db_url = os.environ['DATABASE_URL']
        safe_url = db_url[:30] + "..." + db_url[-20:] if len(db_url) > 50 else db_url
        html += f"<p>DATABASE_URL: {safe_url}</p>"
    
    # Test database connection
    html += f"<h2>Database Connection Test</h2>"
    try:
        with connection.cursor() as cursor:
            # Check if PostgreSQL or SQLite
            if 'postgresql' in connection.vendor:
                html += f"<p class='success'>✅ Using PostgreSQL (correct for production)</p>"
                cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
            else:
                html += f"<p class='error'>❌ Using SQLite (will cause deployment issues)</p>"
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            
            tables = cursor.fetchall()
            html += f"<p>Found {len(tables)} tables:</p><ul>"
            
            required_tables = ['projects_projectcategory', 'projects_project', 'blog_category', 'blog_blogpost']
            existing_tables = [table[0] for table in tables]
            
            for table in tables:
                is_required = table[0] in required_tables
                style = "success" if is_required else ""
                html += f"<li class='{style}'>{table[0]}</li>"
            
            html += "</ul>"
            
            html += f"<h3>Required Tables Status</h3>"
            missing_tables = []
            for req_table in required_tables:
                if req_table in existing_tables:
                    html += f"<p class='success'>✅ {req_table}</p>"
                else:
                    html += f"<p class='error'>❌ {req_table} (MISSING)</p>"
                    missing_tables.append(req_table)
            
            # If tables are missing, try to run migrations
            if missing_tables:
                html += f"<h2>Running Migrations</h2>"
                html += f"<p class='warning'>Missing tables detected. Attempting to run migrations...</p>"
                
                try:
                    # Capture migration output
                    old_stdout = sys.stdout
                    migration_output = io.StringIO()
                    sys.stdout = migration_output
                    
                    call_command('migrate', '--noinput', verbosity=2)
                    
                    sys.stdout = old_stdout
                    output = migration_output.getvalue()
                    
                    html += f"<pre style='background: #f5f5f5; padding: 10px; border-radius: 5px;'>{output}</pre>"
                    html += f"<p class='success'>✅ Migrations completed successfully!</p>"
                    
                    # Try to import projects
                    try:
                        call_command('import_github_projects')
                        html += f"<p class='success'>✅ GitHub projects imported!</p>"
                    except Exception as e:
                        html += f"<p class='warning'>⚠️ Project import failed: {e}</p>"
                    
                    html += f"<p><a href='/projects/'>Try Projects Page Now</a> | <a href='/blog/'>Try Blog Page Now</a></p>"
                    
                except Exception as e:
                    sys.stdout = old_stdout
                    html += f"<p class='error'>❌ Migration failed: {e}</p>"
            else:
                html += f"<p class='success'>✅ All required tables exist!</p>"
                html += f"<p><a href='/projects/'>Projects Page</a> | <a href='/blog/'>Blog Page</a></p>"
                    
    except Exception as e:
        html += f"<p class='error'>❌ Database connection failed: {e}</p>"
    
    html += f"<br><br><p><a href='/' style='background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;'>← Back to Home</a></p>"
    
    return HttpResponse(html)