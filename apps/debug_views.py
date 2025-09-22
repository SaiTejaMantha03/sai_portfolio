"""
Debug view to check database status - only for development/deployment debugging
"""
from django.http import JsonResponse
from django.db import connection
from django.contrib.auth.models import User
from apps.models import Skill
from projects.models import Project, ProjectCategory
from blog.models import Post
from django.conf import settings

def db_status(request):
    """Simple view to check database status"""
    if not settings.DEBUG and not request.user.is_superuser:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_connection = "OK"
    except Exception as e:
        db_connection = f"Error: {str(e)}"

    # Check tables exist
    tables = connection.introspection.table_names()
    required_tables = ['apps_skill', 'projects_project', 'projects_category', 'blog_post']
    missing_tables = [table for table in required_tables if table not in tables]

    # Check data counts
    try:
        data_counts = {
            'users': User.objects.count(),
            'skills': Skill.objects.count(),
            'categories': ProjectCategory.objects.count(),
            'projects': Project.objects.count(),
            'posts': Post.objects.count(),
        }
    except Exception as e:
        data_counts = f"Error: {str(e)}"

    return JsonResponse({
        'database_connection': db_connection,
        'tables_exist': len(missing_tables) == 0,
        'missing_tables': missing_tables,
        'data_counts': data_counts,
        'all_tables': sorted(tables),
    })