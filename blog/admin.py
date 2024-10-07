from django.contrib import admin
from .models import Author, Tag, BlogPost, Category

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'slug')
    search_fields = ('name', 'user__username')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_at', 'is_published')
    list_filter = ('is_published', 'category', 'tags')
    search_fields = ('title', 'content', 'author__name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)