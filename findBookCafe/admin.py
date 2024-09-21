from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import City, Region, Shop, SimplePage, Collection

admin.site.site_header = "Book cafe"
admin.site.index_title = "Welcome to Book Cafe"
admin.site.site_title = "Book cafe"

admin.site.register(City)
admin.site.register(Region)

class ShopAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'order_position')
    ordering = ('order_position',)

admin.site.register(Shop, ShopAdmin)
admin.site.register(SimplePage)
class CollectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'order_position')
    ordering = ('order_position',)

admin.site.register(Collection, CollectionAdmin)