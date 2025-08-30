from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, ProjectCategory, Technology

def project_list(request):
    """Projects list view with filtering"""
    projects = Project.objects.all()
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    # Technology filtering
    tech_id = request.GET.get('technology')
    if tech_id:
        projects = projects.filter(technologies__id=tech_id)
    
    # Status filtering
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(projects, 6)  # Show 6 projects per page
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    # Context data
    categories = ProjectCategory.objects.all()
    technologies = Technology.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    
    context = {
        'projects': projects,
        'categories': categories,
        'technologies': technologies,
        'featured_projects': featured_projects,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tech': tech_id,
        'current_status': status,
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