from django.core.management.base import BaseCommand
from apps.models import Profile, Skill
from blog.models import Category, BlogPost
from projects.models import ProjectCategory, Project, Technology
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
                email="sai@example.com",
                phone="+1234567890",
                location="Your Location",
                github_url="https://github.com/SaiTejaMantha03",
                linkedin_url="https://linkedin.com/in/saitejamantha"
            )

        # Create skills
        skills_data = [
            {"name": "Python", "proficiency": 90, "category": "programming"},
            {"name": "Django", "proficiency": 85, "category": "framework"},
            {"name": "JavaScript", "proficiency": 80, "category": "programming"},
            {"name": "React", "proficiency": 75, "category": "framework"},
            {"name": "MySQL", "proficiency": 70, "category": "database"},
        ]
        
        for skill_data in skills_data:
            Skill.objects.get_or_create(
                name=skill_data["name"],
                defaults=skill_data
            )

        # Create project categories and technologies
        web_cat, _ = ProjectCategory.objects.get_or_create(
            name="Web Development", 
            slug="web-development",
            defaults={"description": "Web development projects"}
        )
        
        django_tech, _ = Technology.objects.get_or_create(
            name="Django",
            defaults={"icon": "fab fa-python", "color": "#092E20"}
        )
        
        python_tech, _ = Technology.objects.get_or_create(
            name="Python",
            defaults={"icon": "fab fa-python", "color": "#3776AB"}
        )

        # Create sample projects based on your actual GitHub repos
        projects_data = [
            {
                "title": "Portfolio Website",
                "slug": "sai-portfolio",
                "description": "A modern portfolio website built with Django featuring blog, projects showcase, and contact functionality. Includes responsive design, admin panel, database integration, and deployment on Render.",
                "short_description": "Modern Django portfolio with blog and projects",
                "category": web_cat,
                "is_featured": True,
                "status": "completed",
                "demo_url": "https://sai-portfolio-nqja.onrender.com",
                "source_url": "https://github.com/SaiTejaMantha03/sai_portfolio"
            },
            {
                "title": "Work Repository",
                "slug": "work-repository",
                "description": "A comprehensive work repository containing various projects, code samples, and development experiments. This repository showcases different programming concepts and implementations.",
                "short_description": "Collection of work projects and code samples",
                "category": web_cat,
                "is_featured": True,
                "status": "completed",
                "demo_url": "",
                "source_url": "https://github.com/SaiTejaMantha03/work"
            },
            {
                "title": "Python Development Projects",
                "slug": "python-projects",
                "description": "A collection of Python projects demonstrating various programming concepts, algorithms, and practical applications. Includes data structures, web scraping, automation scripts, and more.",
                "short_description": "Python programming projects and examples",
                "category": web_cat,
                "is_featured": True,
                "status": "completed",
                "demo_url": "",
                "source_url": "https://github.com/SaiTejaMantha03"
            },
            {
                "title": "Web Development Showcase",
                "slug": "web-development-showcase",
                "description": "A showcase of web development skills including frontend and backend technologies. Features responsive design, modern JavaScript, database integration, and deployment strategies.",
                "short_description": "Full-stack web development demonstrations",
                "category": web_cat,
                "is_featured": False,
                "status": "completed",
                "demo_url": "",
                "source_url": "https://github.com/SaiTejaMantha03"
            },
            {
                "title": "Database Management System",
                "slug": "database-management",
                "description": "A comprehensive database management system built with Python and SQL. Features CRUD operations, data validation, reporting, and user management with secure authentication.",
                "short_description": "Python-based database management system",
                "category": web_cat,
                "is_featured": False,
                "status": "completed",
                "demo_url": "",
                "source_url": "https://github.com/SaiTejaMantha03"
            }
        ]

        for project_data in projects_data:
            project, created = Project.objects.get_or_create(
                slug=project_data["slug"],
                defaults=project_data
            )
            if created:
                project.technologies.add(django_tech, python_tech)

        # Create blog categories and posts
        tech_cat, _ = Category.objects.get_or_create(
            name="Technology",
            slug="technology",
            defaults={"description": "Technology related posts"}
        )
        
        # Create sample blog posts
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            blog_posts = [
                {
                    "title": "My Journey into Full Stack Development",
                    "slug": "my-journey-full-stack-development",
                    "content": "Starting my career in software development has been an incredible journey. From learning Python basics to building complex web applications with Django, every step has taught me something new. In this post, I'll share my experiences, challenges, and the technologies that have shaped my development skills.",
                    "excerpt": "My personal journey and experiences in full stack development",
                    "category": tech_cat,
                    "author": admin_user,
                    "status": "published",
                    "is_published": True
                },
                {
                    "title": "Building Modern Web Applications with Django",
                    "slug": "building-modern-web-applications-django",
                    "content": "Django is a powerful Python web framework that enables rapid development of secure and maintainable websites. In this comprehensive guide, I'll walk you through the process of building a modern web application from scratch, covering models, views, templates, and deployment strategies.",
                    "excerpt": "Complete guide to building web applications with Django framework",
                    "category": tech_cat,
                    "author": admin_user,
                    "status": "published",
                    "is_published": True
                },
                {
                    "title": "Database Design Best Practices",
                    "slug": "database-design-best-practices",
                    "content": "Proper database design is crucial for building scalable applications. This post covers normalization, indexing, relationships, and performance optimization techniques that every developer should know when working with databases.",
                    "excerpt": "Essential database design principles for developers",
                    "category": tech_cat,
                    "author": admin_user,
                    "status": "published",
                    "is_published": True
                },
                {
                    "title": "Deploying Applications to the Cloud",
                    "slug": "deploying-applications-cloud",
                    "content": "Cloud deployment has revolutionized how we ship applications. Learn about different deployment strategies, containerization with Docker, and platforms like Render, Heroku, and AWS for hosting your web applications.",
                    "excerpt": "Modern deployment strategies and cloud platforms",
                    "category": tech_cat,
                    "author": admin_user,
                    "status": "published",
                    "is_published": True
                }
            ]
            
            for post_data in blog_posts:
                BlogPost.objects.get_or_create(
                    slug=post_data["slug"],
                    defaults=post_data
                )

        self.stdout.write('Sample data loaded successfully')