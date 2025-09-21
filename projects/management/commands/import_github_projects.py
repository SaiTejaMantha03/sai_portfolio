import json
import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from datetime import datetime
from projects.models import Project, ProjectCategory, Technology


class Command(BaseCommand):
    help = 'Import projects from GitHub repositories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='SaiTejaMantha03',
            help='GitHub username to fetch repositories from'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        self.stdout.write(f"Fetching repositories for {username}...")
        
        try:
            # Fetch repositories from GitHub API
            response = requests.get(f'https://api.github.com/users/{username}/repos?per_page=100')
            response.raise_for_status()
            repos = response.json()
            
            self.stdout.write(f"Found {len(repos)} repositories")
            
            # Create or get default category
            web_category, created = ProjectCategory.objects.get_or_create(
                name="Web Development",
                defaults={
                    'slug': 'web-development',
                    'description': 'Web development projects and applications'
                }
            )
            
            data_science_category, created = ProjectCategory.objects.get_or_create(
                name="Data Science",
                defaults={
                    'slug': 'data-science',
                    'description': 'Data analysis and machine learning projects'
                }
            )
            
            network_category, created = ProjectCategory.objects.get_or_create(
                name="Computer Networks",
                defaults={
                    'slug': 'computer-networks',
                    'description': 'Network programming and protocols'
                }
            )
            
            # Create technologies
            technologies_map = {
                'Python': {'color': '#3776ab', 'icon': 'fab fa-python'},
                'HTML': {'color': '#e34c26', 'icon': 'fab fa-html5'},
                'JavaScript': {'color': '#f7df1e', 'icon': 'fab fa-js-square'},
                'CSS': {'color': '#1572b6', 'icon': 'fab fa-css3-alt'},
                'Jupyter Notebook': {'color': '#f37626', 'icon': 'fas fa-book'},
                'Tcl': {'color': '#007bff', 'icon': 'fas fa-code'},
                'Django': {'color': '#092e20', 'icon': 'fas fa-server'},
            }
            
            for tech_name, tech_info in technologies_map.items():
                Technology.objects.get_or_create(
                    name=tech_name,
                    defaults={
                        'color': tech_info['color'],
                        'icon': tech_info['icon']
                    }
                )
            
            # Process each repository
            for repo in repos:
                # Skip the portfolio repo itself
                if repo['name'] == 'sai_portfolio':
                    continue
                    
                # Determine category based on language and name
                language = repo.get('language', '').lower()
                repo_name = repo['name'].lower()
                
                if 'spam' in repo_name or 'classifier' in repo_name or language == 'jupyter notebook':
                    category = data_science_category
                elif 'cn' in repo_name or 'network' in repo_name or language == 'tcl':
                    category = network_category
                else:
                    category = web_category
                
                # Create or update project
                project, created = Project.objects.get_or_create(
                    title=repo['name'].replace('-', ' ').replace('_', ' ').title(),
                    defaults={
                        'slug': slugify(repo['name']),
                        'description': self.generate_description(repo),
                        'short_description': repo.get('description', f"GitHub repository: {repo['name']}") or f"GitHub repository: {repo['name']}",
                        'source_url': repo['html_url'],
                        'category': category,
                        'status': 'completed',
                        'is_featured': repo['stargazers_count'] > 0,
                        'github_stars': repo['stargazers_count'],
                    }
                )
                
                if not created:
                    # Update existing project
                    project.github_stars = repo['stargazers_count']
                    project.is_featured = repo['stargazers_count'] > 0
                    project.save()
                
                # Add technologies
                if repo.get('language'):
                    try:
                        tech = Technology.objects.get(name=repo['language'])
                        project.technologies.add(tech)
                    except Technology.DoesNotExist:
                        pass
                
                # Add Django technology for Python projects that might be Django
                if repo.get('language') == 'Python' and 'portfolio' in repo['name'].lower():
                    try:
                        django_tech = Technology.objects.get(name='Django')
                        project.technologies.add(django_tech)
                    except Technology.DoesNotExist:
                        pass
                
                action = "Created" if created else "Updated"
                self.stdout.write(
                    self.style.SUCCESS(f'{action} project: {project.title}')
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported/updated projects from GitHub!')
            )
            
        except requests.RequestException as e:
            self.stdout.write(
                self.style.ERROR(f'Error fetching repositories: {e}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error processing repositories: {e}')
            )
    
    def generate_description(self, repo):
        """Generate a detailed description for the project"""
        description = repo.get('description', '')
        
        # Enhanced descriptions based on repo name
        repo_name = repo['name'].lower()
        
        if 'civic' in repo_name and 'system' in repo_name:
            return "A civic redressal system designed to help citizens report and track civic issues. Built with modern web technologies to provide an efficient platform for community engagement and issue resolution."
        
        elif 'spam' in repo_name and 'classifier' in repo_name:
            return "A machine learning project focused on spam classification using data analysis techniques. Implements various algorithms to accurately identify and filter spam messages, demonstrating practical applications of natural language processing."
        
        elif 'cn' in repo_name or 'network' in repo_name:
            return "Computer Networks laboratory assignments and projects. Includes implementations of network protocols, socket programming, and network simulation experiments using various tools and technologies."
        
        elif 'lab' in repo_name:
            return "Collection of laboratory assignments and programming exercises. Contains various coding challenges and solutions developed during academic coursework."
        
        elif 'portfolio' in repo_name:
            return "Personal portfolio website built with Django framework. Showcases projects, skills, and professional experience with a clean, responsive design and modern web development practices."
        
        else:
            return description or f"A {repo.get('language', 'programming')} project showcasing development skills and technical expertise."