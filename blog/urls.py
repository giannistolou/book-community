from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<slug:post_slug>/', views.post, name='post_detail'),
    path('tag/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),
    path('author/<slug:author_slug>/', views.posts_by_author, name='posts_by_author'),
    path('category/<slug:category_slug>/', views.posts_by_category, name='posts_by_category'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
