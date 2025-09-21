#!/usr/bin/env python
"""
Post-deployment script to populate the database with projects.
Run this after the first deployment to add your projects.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from projects.models import Project, ProjectCategory, Technology

def populate_database():
    print("🚀 Populating database with projects...")
    
    # Create categories
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
    
    # Create technologies
    python_tech, created = Technology.objects.get_or_create(
        name="Python",
        defaults={'color': '#3776ab', 'icon': 'fab fa-python'}
    )
    
    html_tech, created = Technology.objects.get_or_create(
        name="HTML",
        defaults={'color': '#e34c26', 'icon': 'fab fa-html5'}
    )
    
    jupyter_tech, created = Technology.objects.get_or_create(
        name="Jupyter Notebook",
        defaults={'color': '#f37626', 'icon': 'fas fa-book'}
    )
    
    # Create projects
    projects_data = [
        {
            'title': 'Medical Laboratory System',
            'slug': 'medical-laboratory-system',
            'description': 'A sophisticated medical laboratory management system designed to streamline laboratory operations in healthcare facilities.',
            'short_description': 'A comprehensive medical laboratory management system for handling test results, patient data, and medical diagnostics.',
            'source_url': 'https://github.com/SaiTejaMantha03/lab',
            'category': web_category,
            'technology': python_tech,
        },
        {
            'title': 'Spam Classifier',
            'slug': 'spam-classifier', 
            'description': 'A machine learning project focused on spam classification using data analysis techniques.',
            'short_description': 'Learning Data Analysis and implementing spam detection algorithms.',
            'source_url': 'https://github.com/SaiTejaMantha03/Spam-Classifier',
            'category': data_science_category,
            'technology': jupyter_tech,
        },
        {
            'title': 'Civic Readdressal System',
            'slug': 'civic-readdressal-system',
            'description': 'A civic redressal system designed to help citizens report and track civic issues.',
            'short_description': 'A platform for community engagement and civic issue resolution.',
            'source_url': 'https://github.com/SaiTejaMantha03/Civic-ReAddressal-System',
            'category': web_category,
            'technology': html_tech,
        }
    ]
    
    for project_data in projects_data:
        technology = project_data.pop('technology')
        project, created = Project.objects.get_or_create(
            slug=project_data['slug'],
            defaults={
                **project_data,
                'status': 'completed',
                'is_featured': False,
                'github_stars': 0,
            }
        )
        
        if created:
            project.technologies.add(technology)
            print(f"✅ Created project: {project.title}")
        else:
            print(f"⏭️ Project already exists: {project.title}")
    
    print("🎉 Database population complete!")

if __name__ == '__main__':
    populate_database()