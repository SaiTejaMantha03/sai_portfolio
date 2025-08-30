from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, Category, Tag

def blog_list(request):
    """Blog list view with pagination and filtering"""
    posts = BlogPost.objects.filter(is_published=True)
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Tag filtering
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    # Context data
    categories = Category.objects.all()
    tags = Tag.objects.all()
    recent_posts = BlogPost.objects.filter(is_published=True)[:5]
    
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tag': tag_slug,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    """Blog detail view"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    
    # Increment view count
    post.views_count += 1
    post.save(update_fields=['views_count'])
    
    # Get related posts
    related_posts = BlogPost.objects.filter(
        is_published=True,
        category=post.category
    ).exclude(id=post.id)[:3]
    
    # Get comments
    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }
    return render(request, 'blog/blog_detail.html', context)

def category_posts(request, slug):
    """Category-wise blog posts"""
    category = get_object_or_404(Category, slug=slug)
    posts = BlogPost.objects.filter(category=category, is_published=True)
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'blog/category_posts.html', context)