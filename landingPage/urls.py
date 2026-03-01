from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static
from landingPage.views import subscribe, thank_you_subscribe

urlpatterns = [
    path('', views.bio, name='index'),
    path('bio/', views.bio, name='bio'),
    # TODO make it universal
    path("newsletter-subscribe/", subscribe, name="newsletter_subscribe"),
    path('thank-you-subscribe/', thank_you_subscribe, name='thank_you_subscribe'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)