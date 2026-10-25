import html
import json
import re

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

register = template.Library()

STRUCTURED_DATA_TYPES = {'CAF': 'CafeOrCoffeeShop', 'LIB': 'Library'}


@register.filter
def meta_description(value, length=155):
    """Plain-text summary of rich text for <meta name="description">."""
    text = re.sub(r'\s+', ' ', html.unescape(strip_tags(str(value or '')))).strip()
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0].rstrip(' ,.;:') + '…'


def _json_ld(data):
    # Escaping "<" keeps a "</script>" inside any field from closing the tag
    payload = json.dumps(data, ensure_ascii=False, indent=2).replace('<', '\\u003c')
    return mark_safe(f'<script type="application/ld+json">\n{payload}\n</script>')


@register.simple_tag(takes_context=True)
def shop_structured_data(context, shop):
    data = {
        '@context': 'https://schema.org',
        '@type': STRUCTURED_DATA_TYPES.get(shop.type, 'LocalBusiness'),
        'name': shop.name,
        'url': context.get('canonical_url', ''),
        'description': meta_description(shop.description, 300),
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': shop.address,
        },
        'geo': {
            '@type': 'GeoCoordinates',
            'latitude': shop.latitude,
            'longitude': shop.longitude,
        },
    }
    if shop.region:
        data['address']['addressLocality'] = shop.region.name
        data['address']['addressRegion'] = shop.region.city.name
    if shop.thumbnail:
        data['image'] = f"{context.get('SITE_ORIGIN', '')}/media/{shop.thumbnail}"
    if shop.googleMaps:
        data['hasMap'] = shop.googleMaps
    same_as = [url for url in (shop.website, shop.facebook, shop.instagram, shop.tripadvisor) if url]
    if same_as:
        data['sameAs'] = same_as
    return _json_ld(data)
