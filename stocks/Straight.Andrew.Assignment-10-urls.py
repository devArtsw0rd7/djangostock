# Define URL patterns for stocks

from django.urls import path
from . import StraightAndrewAssignment10views

# App namespace
app_name = 'stocks'

# Url paths for each page
urlpatterns = [
    path('', StraightAndrewAssignment10views.index, name='index'),
    path('about/', StraightAndrewAssignment10views.about, name='about'),
    path('add_stock/', StraightAndrewAssignment10views.add_stock, name='add_stock'),
    path('delete/<stock_id>', StraightAndrewAssignment10views.delete, name='delete'),
    path('remove_stock/', StraightAndrewAssignment10views.remove_stock, name='remove_stock'),
    path('register/', StraightAndrewAssignment10views.register, name='register'),
    path('login/', StraightAndrewAssignment10views.login_request, name='login'),
    path('logout/', StraightAndrewAssignment10views.logout_request, name='logout'),
]
