from django.conf import settings
from landingPage.forms import SubscribeForm
from bookCommunity import settings as settings_app

def book_cafe_domain(request):
    return {"BOOK_CAFE_DOMAIN": settings.BOOK_CAFE_DOMAIN}

def is_debug_mode(request):
    return {"DEBUG": settings.DEBUG}

def common_data(request):
    return {
        'subscribe_form': SubscribeForm(),
        'TURNSTILE_SITE_KEY': getattr(settings, 'TURNSTILE_SITE_KEY', ''),
    }

def seo(request):
    # Production is always served over HTTPS, even if a proxy header goes missing
    scheme = request.scheme if settings.DEBUG else 'https'
    host = request.get_host().removeprefix('www.')
    origin = f"{scheme}://{host}"
    canonical_url = origin + request.path
    page = request.GET.get('page', '')
    if page.isdigit() and page != '1':
        canonical_url += f"?page={page}"
    return {'SITE_ORIGIN': origin, 'canonical_url': canonical_url}
