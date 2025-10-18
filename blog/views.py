from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import BlogPost, Category, Tag

def blog_list(request):
    """Blog list view with pagination and filtering"""
    try:
        posts = BlogPost.objects.all()  # Show all posts including drafts
        categories = Category.objects.all()
        tags = Tag.objects.all()
        recent_posts = BlogPost.objects.all()[:5]
    except Exception as e:
        # Database connection failed - provide fallback content
        posts = []
        categories = []
        tags = []
        recent_posts = []
        print(f"Database connection failed in blog_list: {e}")
    
    context = {
        'posts': posts,
        'categories': categories,
        'tags': tags,
        'recent_posts': recent_posts,
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