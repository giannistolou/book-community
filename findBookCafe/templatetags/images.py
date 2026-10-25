from django import template

from findBookCafe.thumbnails import best_thumbnail, existing_thumbnails

register = template.Library()


@register.simple_tag
def thumbnail(image, width):
    return best_thumbnail(str(image or ''), int(width))


@register.simple_tag
def thumbnail_srcset(image, media_url):
    thumbnails = existing_thumbnails(str(image or ''))
    return ', '.join(f"{media_url}{name} {width}w" for width, name in sorted(thumbnails.items()))
