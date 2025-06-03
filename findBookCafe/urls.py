from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.map, name='map'),
    path('collections/', views.collections, name="collections"),
    path('collections/<str:page_slug>/', views.collection, name="collection"),
    path('page/<str:page_slug>/', views.simple_page, name='page'),
    path('<str:type>/', views.cafes, name='cafes'),
    path('<str:type>/<str:city>/', views.cafe_city, name='city'),
    path('<str:type>/<str:city>/<str:region>/', views.cafe_region, name='region'),
    path('<str:type>/<str:city>/<str:region>/<str:cafe>/', views.cafe, name='cafe'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)