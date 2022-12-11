from django.contrib import admin
from .models import City, Region, Shop, SimplePage

admin.site.site_header = "Book cafe"
admin.site.index_title = "Welcome to Book Cafe"
admin.site.site_title = "Book cafe"



admin.site.register(City)
admin.site.register(Region)
admin.site.register(Shop)
admin.site.register(SimplePage)