from django import template

from findBookCafe.thumbnails import ensure_thumbnails

register = template.Library()


@register.simple_tag
def thumbnail(image, width):
    """Name of the closest WebP thumbnail not narrower than width, or the original."""
    name = str(image or '')
    thumbnails = ensure_thumbnails(name)
    for thumb_width in sorted(thumbnails):
        if thumb_width >= int(width):
            return thumbnails[thumb_width]
    return thumbnails[max(thumbnails)] if thumbnails else name


@register.simple_tag
def thumbnail_srcset(image, media_url):
    thumbnails = ensure_thumbnails(str(image or ''))
    return ', '.join(f"{media_url}{name} {width}w" for width, name in sorted(thumbnails.items()))
