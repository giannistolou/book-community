from django_hosts import patterns, host
from django.conf import settings

host_patterns = patterns('',
    host(r'^$', settings.ROOT_URLCONF, name='www'),
    host(r'cafe', 'findBookCafe.urls', name='cafe'),
    # TODO change to blog
    host(r'blog2', 'blog.urls', name='blog'),
)