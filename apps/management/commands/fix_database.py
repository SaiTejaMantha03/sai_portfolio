from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Fix database issues by ensuring all tables exist and data is populated'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Starting database repair...'))
        
        # Check current database state
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(f'📊 Found {len(tables)} tables before repair')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'❌ Database error: {e}'))
        
        # Force migrations
        self.stdout.write('🗄️ Running migrations...')
        try:
            call_command('migrate', '--noinput', verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Migrations completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Migration error: {e}'))
        
        # Check database state after migrations
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(f'📊 Found {len(tables)} tables after migrations:')
                for table in tables:
                    self.stdout.write(f'  - {table[0]}')
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'❌ Database check error: {e}'))
        
        # Import GitHub projects
        self.stdout.write('📊 Importing projects...')
        try:
            call_command('import_github_projects')
            self.stdout.write(self.style.SUCCESS('✅ Projects imported'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'⚠️ Project import failed: {e}'))
        
        self.stdout.write(self.style.SUCCESS('🎉 Database repair complete!'))