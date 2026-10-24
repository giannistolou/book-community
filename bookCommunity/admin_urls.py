from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', admin.site.urls),
]

handler404 = 'findBookCafe.views.page404'
handler500 = 'findBookCafe.views.page500'
