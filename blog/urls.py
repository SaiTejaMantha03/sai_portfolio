from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('<slug:slug>/', views.blog_detail, name='post_detail'),
]