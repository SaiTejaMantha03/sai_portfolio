from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, ProjectCategory, Technology

def project_list(request):
    """Projects list view with filtering"""
    try:
        projects = Project.objects.all()
        categories = ProjectCategory.objects.all()
        technologies = Technology.objects.all()
        featured_projects = Project.objects.filter(is_featured=True)[:3]
    except Exception as e:
        # Database connection failed - provide fallback content
        projects = []
        categories = []
        technologies = []
        featured_projects = []
        print(f"Database connection failed in project_list: {e}")
    
    context = {
        'projects': projects,
        'categories': categories,
        'technologies': technologies,
        'featured_projects': featured_projects,
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, slug):
    """Project detail view"""
    project = get_object_or_404(Project, slug=slug)
    
    # Increment view count
    project.views_count += 1
    project.save(update_fields=['views_count'])
    
    # Get related projects
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)

def category_projects(request, slug):
    """Category-wise projects"""
    category = get_object_or_404(ProjectCategory, slug=slug)
    projects = Project.objects.filter(category=category)
    
    paginator = Paginator(projects, 6)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context = {
        'projects': projects,
        'category': category,
    }
    return render(request, 'projects/category_projects.html', context)