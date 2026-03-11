from django.conf import settings
from landingPage.forms import SubscribeForm
from bookCommunity import settings as settings_app

def book_cafe_domain(request):
    return {"BOOK_CAFE_DOMAIN": settings.BOOK_CAFE_DOMAIN}

def is_debug_mode(request):
    return {"DEBUG": settings.DEBUG}

def common_data(request):
    return {
        'form': SubscribeForm(),
        'TURNSTILE_SITE_KEY': settings_app.TURNSTILE_SITE_KEY,
    }