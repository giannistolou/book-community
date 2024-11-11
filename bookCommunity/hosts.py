from django_hosts import patterns, host
from django.conf import settings
from django.contrib import admin

host_patterns = patterns('',
    host(r'^$', settings.ROOT_URLCONF, name='www'),
    host(r'cafe', 'findBookCafe.urls', name='cafe'),
    host(r'blog', 'blog.urls', name='blog'),
)