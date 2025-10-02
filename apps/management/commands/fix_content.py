from django.core.management.base import BaseCommand
from apps.models import Profile
from blog.models import BlogPost
from projects.models import Project

class Command(BaseCommand):
    help = 'Fix profile image and remove unnecessary projects'

    def handle(self, *args, **options):
        # Update profile with correct image path
        profile, created = Profile.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Sai Teja Mantha',
                'title': 'Full Stack Developer',
                'description': 'Passionate full stack developer with experience in web development, mobile applications, and cloud technologies.',
                'email': 'saitejamantha@example.com',
                'profile_image': '/media/profile/1730075781405.jpeg',
                'resume': '/media/resume/Untitled_document.pdf',
                'github_url': 'https://github.com/saitejamantha',
                'linkedin_url': 'https://linkedin.com/in/saitejamantha',
            }
        )

        if not created:
            profile.profile_image = '/media/profile/1730075781405.jpeg'
            profile.resume = '/media/resume/Untitled_document.pdf'
            profile.save()

        self.stdout.write(
            self.style.SUCCESS(f'Profile updated: {profile.name}')
        )
        self.stdout.write(f'Image path: {profile.profile_image}')

        # Remove unnecessary sample projects (keep only the portfolio project)
        projects_to_remove = Project.objects.exclude(title__icontains='Portfolio')
        removed_count = projects_to_remove.count()
        
        if removed_count > 0:
            for project in projects_to_remove:
                self.stdout.write(f'Removing project: {project.title}')
            projects_to_remove.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Removed {removed_count} unnecessary projects')
            )
        else:
            self.stdout.write('No unnecessary projects to remove')

        # List remaining projects
        remaining_projects = Project.objects.all()
        self.stdout.write(f'Remaining projects: {remaining_projects.count()}')
        for project in remaining_projects:
            self.stdout.write(f'  - {project.title}')