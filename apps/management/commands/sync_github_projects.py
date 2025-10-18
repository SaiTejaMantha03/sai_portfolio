from django.core.management.base import BaseCommand
from projects.models import ProjectCategory, Project, Technology
import requests
import json

class Command(BaseCommand):
    help = 'Sync projects from GitHub'

    def handle(self, *args, **options):
        github_username = "SaiTejaMantha03"
        
        try:
            # Fetch repositories from GitHub API
            url = f"https://api.github.com/users/{github_username}/repos"
            response = requests.get(url)
            
            if response.status_code == 200:
                repos = response.json()
                
                # Create default category
                web_cat, _ = ProjectCategory.objects.get_or_create(
                    name="GitHub Projects", 
                    slug="github-projects",
                    defaults={"description": "Projects from GitHub"}
                )
                
                # Create technologies
                python_tech, _ = Technology.objects.get_or_create(
                    name="Python",
                    defaults={"icon": "fab fa-python", "color": "#3776AB"}
                )
                
                js_tech, _ = Technology.objects.get_or_create(
                    name="JavaScript",
                    defaults={"icon": "fab fa-js", "color": "#F7DF1E"}
                )
                
                # Process repositories
                for repo in repos[:10]:  # Limit to 10 repos
                    if not repo['fork'] and repo['description']:  # Skip forks and repos without description
                        
                        # Determine if featured (has stars or is recent)
                        is_featured = repo['stargazers_count'] > 0 or 'portfolio' in repo['name'].lower()
                        
                        # Create or update project
                        project, created = Project.objects.get_or_create(
                            slug=repo['name'].lower().replace('_', '-'),
                            defaults={
                                'title': repo['name'].replace('_', ' ').replace('-', ' ').title(),
                                'description': repo['description'] or 'GitHub repository',
                                'short_description': (repo['description'] or 'GitHub repository')[:200],
                                'category': web_cat,
                                'demo_url': repo['homepage'] or '',
                                'source_url': repo['html_url'],
                                'is_featured': is_featured,
                                'status': 'completed',
                                'github_stars': repo['stargazers_count'],
                            }
                        )
                        
                        if created:
                            # Add technologies based on language
                            if repo['language']:
                                if repo['language'].lower() in ['python']:
                                    project.technologies.add(python_tech)
                                elif repo['language'].lower() in ['javascript', 'html', 'css']:
                                    project.technologies.add(js_tech)
                
                self.stdout.write(f'Successfully synced {len(repos)} repositories from GitHub')
            else:
                self.stdout.write('Failed to fetch repositories from GitHub')
                
        except Exception as e:
            self.stdout.write(f'Error syncing GitHub projects: {str(e)}')