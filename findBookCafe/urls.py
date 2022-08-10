from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('cafes', views.cafes, name='cafes'),
    path('libraries', views.libraries, name='libraries'),
    path('cafes/<str:cafe>', views.cafe, name='cafe'),
    path('map', views.map, name='map'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)