from django.urls import path
from . import views
from . import debug_views

app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('photos/', views.photos, name='photos'),
    path('debug/database/', debug_views.debug_database, name='debug_database'),
]