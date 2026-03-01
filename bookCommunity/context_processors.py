from django.conf import settings

def book_cafe_domain(request):
    return {"BOOK_CAFE_DOMAIN": settings.BOOK_CAFE_DOMAIN}

def is_debug_mode(request):
    return {"DEBUG": settings.DEBUG}