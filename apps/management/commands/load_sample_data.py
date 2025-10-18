from django.core.management.base import BaseCommand
from apps.models import Profile, Skill
from blog.models import Category, BlogPost
from projects.models import ProjectCategory, Project
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load sample data'

    def handle(self, *args, **options):
        # Create sample profile
        if not Profile.objects.exists():
            Profile.objects.create(
                name="Sai Teja Mantha",
                title="Full Stack Developer",
                description="Passionate developer with expertise in web technologies",
                email="sai@example.com"
            )

        # Create sample projects
        if not Project.objects.exists():
            cat, _ = ProjectCategory.objects.get_or_create(name="Web Development", slug="web-dev")
            Project.objects.create(
                title="Portfolio Website",
                slug="portfolio-website",
                description="Personal portfolio built with Django",
                short_description="Modern portfolio website",
                category=cat,
                is_featured=True,
                status="completed"
            )

        self.stdout.write('Sample data loaded successfully')