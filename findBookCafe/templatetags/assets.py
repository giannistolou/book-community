import logging
import posixpath
import re
from functools import lru_cache

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)
register = template.Library()

RELATIVE_CSS_URL = re.compile(r'url\(\s*([\'"]?)(?!data:|https?:|/|#)([^\'")]+)\1\s*\)')
SOURCE_MAP_COMMENT = re.compile(r'/\*# sourceMappingURL=.*?\*/')


def _read_css(name):
    if settings.DEBUG:
        path = finders.find(name)
    else:
        path = staticfiles_storage.path(staticfiles_storage.stored_name(name))
    with open(path, encoding='utf-8') as css_file:
        css = SOURCE_MAP_COMMENT.sub('', css_file.read())
    # url()s are relative to the stylesheet, which no longer applies once the CSS sits in the page
    base = posixpath.dirname(static(name))
    css = RELATIVE_CSS_URL.sub(lambda m: f'url({m[1]}{posixpath.normpath(posixpath.join(base, m[2]))}{m[1]})', css)
    return css.replace('</style', '<\\/style')


_cached_css = lru_cache(maxsize=None)(_read_css)


@register.simple_tag
def inline_css(name):
    """Inline a small stylesheet so it does not block the first paint with an extra request."""
    try:
        css = _read_css(name) if settings.DEBUG else _cached_css(name)
    except (OSError, ValueError):
        logger.warning("Cannot inline %s, linking it instead", name, exc_info=True)
        return format_html('<link rel="stylesheet" href="{}" />', static(name))
    return mark_safe(f'<style>{css}</style>')
