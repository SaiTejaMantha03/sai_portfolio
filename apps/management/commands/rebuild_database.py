from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Force reset and rebuild all database tables and data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reset even if tables exist',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting database rebuild...'))
        
        # Show current database info
        db_config = connection.settings_dict
        self.stdout.write(f"📍 Database Engine: {db_config['ENGINE']}")
        self.stdout.write(f"📍 Database Name: {db_config.get('NAME', 'N/A')}")
        
        # Check if we're using PostgreSQL
        if 'postgresql' in db_config['ENGINE']:
            self.stdout.write(self.style.SUCCESS('✅ Using PostgreSQL - this is correct for production'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Not using PostgreSQL - this may cause issues'))
        
        # Force migrations
        self.stdout.write('🗄️ Running migrations...')
        try:
            call_command('migrate', '--noinput', verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migration error: {e}'))
            return
        
        # Check tables exist
        try:
            with connection.cursor() as cursor:
                if 'postgresql' in connection.vendor:
                    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                else:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                
                required_tables = ['projects_projectcategory', 'projects_project', 'blog_category', 'blog_blogpost']
                existing_tables = [table[0] for table in tables]
                
                self.stdout.write(f'📊 Found {len(tables)} total tables')
                
                missing_tables = [table for table in required_tables if table not in existing_tables]
                if missing_tables:
                    self.stdout.write(self.style.ERROR(f'❌ Missing required tables: {missing_tables}'))
                else:
                    self.stdout.write(self.style.SUCCESS('✅ All required tables exist'))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database check error: {e}'))
            return
        
        # Import projects
        self.stdout.write('📊 Importing GitHub projects...')
        try:
            call_command('import_github_projects')
            self.stdout.write(self.style.SUCCESS('✅ Projects imported'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️ Project import failed: {e}'))
        
        self.stdout.write(self.style.SUCCESS('🎉 Database rebuild complete!'))