"""
Management command to check database status and setup production data
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from apps.models import Skill
from projects.models import Project, ProjectCategory
from blog.models import Post
import os

class Command(BaseCommand):
    help = 'Check database status and setup production data if needed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--setup',
            action='store_true',
            help='Setup production data',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking database status...'))
        
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('✅ Database connection: OK'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Database connection error: {e}'))
            return

        # Check tables exist
        tables = connection.introspection.table_names()
        required_tables = ['apps_skill', 'projects_project', 'projects_category', 'blog_post']
        
        missing_tables = [table for table in required_tables if table not in tables]
        if missing_tables:
            self.stdout.write(self.style.WARNING(f'⚠️  Missing tables: {missing_tables}'))
            self.stdout.write(self.style.WARNING('Run migrations first: python manage.py migrate'))
        else:
            self.stdout.write(self.style.SUCCESS('✅ All required tables exist'))

        # Check data counts
        try:
            skill_count = Skill.objects.count()
            project_count = Project.objects.count()
            category_count = ProjectCategory.objects.count()
            post_count = Post.objects.count()
            user_count = User.objects.count()

            self.stdout.write(self.style.SUCCESS(f'📊 Data counts:'))
            self.stdout.write(f'   Users: {user_count}')
            self.stdout.write(f'   Skills: {skill_count}')
            self.stdout.write(f'   Categories: {category_count}')
            self.stdout.write(f'   Projects: {project_count}')
            self.stdout.write(f'   Blog posts: {post_count}')

            if options['setup'] and project_count == 0:
                self.stdout.write(self.style.WARNING('🔄 Setting up initial data...'))
                self.setup_initial_data()
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error checking data: {e}'))

    def setup_initial_data(self):
        """Setup initial data for production"""
        from django.core.management import call_command
        
        try:
            # Create superuser if none exists
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'  # Change this in production!
                )
                self.stdout.write(self.style.SUCCESS('✅ Created superuser (admin/admin123)'))

            # Import GitHub projects
            self.stdout.write(self.style.SUCCESS('🔄 Importing GitHub projects...'))
            call_command('import_github_projects')
            
            # Create some skills if none exist
            if not Skill.objects.exists():
                skills_data = [
                    {'name': 'Python', 'proficiency': 90},
                    {'name': 'Django', 'proficiency': 85},
                    {'name': 'JavaScript', 'proficiency': 80},
                    {'name': 'React', 'proficiency': 75},
                    {'name': 'PostgreSQL', 'proficiency': 80},
                    {'name': 'HTML/CSS', 'proficiency': 90},
                ]
                
                for skill_data in skills_data:
                    Skill.objects.get_or_create(
                        name=skill_data['name'],
                        defaults={'proficiency': skill_data['proficiency']}
                    )
                self.stdout.write(self.style.SUCCESS('✅ Created initial skills'))

            self.stdout.write(self.style.SUCCESS('🎉 Initial data setup complete!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error setting up data: {e}'))