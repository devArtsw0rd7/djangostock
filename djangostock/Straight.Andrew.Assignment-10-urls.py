# djangostock URL Configuration

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stocks.Straight.Andrew.Assignment-10-urls')),
]
