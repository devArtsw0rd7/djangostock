# Define URL patterns for stocks

from django.urls import path
from . import views

app_name = 'stocks'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('delete/<stock_id>', views.delete, name="delete"),
    path('remove_stock/', views.remove_stock, name="remove_stock")
]
