from django.db import models
from django.urls import reverse

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Project Categories"

    def __str__(self):
        return self.name

class Technology(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")

    class Meta:
        verbose_name_plural = "Technologies"

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    short_description = models.TextField(max_length=300, help_text="Brief project description")
    featured_image = models.ImageField(upload_to='projects/', blank=True, null=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True)
    
    # Project Links
    demo_url = models.URLField(blank=True, help_text="Live demo URL")
    source_url = models.URLField(blank=True, help_text="Source code URL (GitHub, etc.)")
    
    # Project Status and Features
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='planning')
    is_featured = models.BooleanField(default=False)
    is_personal = models.BooleanField(default=True)
    client_name = models.CharField(max_length=100, blank=True)
    
    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Metrics
    views_count = models.PositiveIntegerField(default=0)
    github_stars = models.PositiveIntegerField(default=0, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['is_featured']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:project_detail', kwargs={'slug': self.slug})

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.project.title}"

class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.project.title}"