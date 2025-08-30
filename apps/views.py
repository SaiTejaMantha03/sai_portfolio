from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Profile, Skill, Experience, Education
from blog.models import BlogPost
from projects.models import Project

def home(request):
    """Home page view"""
    try:
        profile = Profile.objects.first()
        skills = Skill.objects.all()
        recent_projects = Project.objects.filter(is_featured=True)[:3]
        recent_blogs = BlogPost.objects.filter(is_published=True)[:3]
    except:
        # Handle case when tables don't exist yet
        profile = None
        skills = []
        recent_projects = []
        recent_blogs = []
    
    context = {
        'profile': profile,
        'skills': skills,
        'recent_projects': recent_projects,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'portfolio/index.html', context)

def about(request):
    """About page view"""
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    education = Education.objects.all()
    
    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'education': education,
    }
    return render(request, 'portfolio/about.html', context)

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you can add email sending logic
        # For now, just return success
        return JsonResponse({'success': True})
    
    try:
        profile = Profile.objects.first()
    except Profile.DoesNotExist:
        profile = None
    
    context = {'profile': profile}
    return render(request, 'portfolio/contact.html', context)

def photos(request):
    """Photos page view"""
    return render(request, 'portfolio/photos.html')