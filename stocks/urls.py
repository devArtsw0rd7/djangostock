# Define URL patterns for stocks

from django.urls import path
from . import views

# App namespace
app_name = 'stocks'

# Url paths for each page
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add_stock/', views.add_stock, name='add_stock'),
    path('delete/<stock_id>', views.delete, name='delete'),
    path('remove_stock/', views.remove_stock, name='remove_stock'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
]
