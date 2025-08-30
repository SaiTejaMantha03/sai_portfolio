from django.contrib import admin
from .models import Project, ProjectCategory, Technology, ProjectImage, ProjectFeature

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1

class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color']
    search_fields = ['name']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'created_at', 'views_count']
    list_filter = ['status', 'is_featured', 'is_personal', 'category', 'created_at']
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [ProjectImageInline, ProjectFeatureInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'short_description')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Organization', {
            'fields': ('category', 'technologies')
        }),
        ('Links', {
            'fields': ('demo_url', 'source_url')
        }),
        ('Status & Dates', {
            'fields': ('status', 'start_date', 'end_date', 'is_featured', 'is_personal', 'client_name')
        }),
        ('Metrics', {
            'fields': ('views_count', 'github_stars'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'is_featured', 'order']
    list_filter = ['is_featured', 'project']

@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'order']
    list_filter = ['project']