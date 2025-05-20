from django.urls import path
from . import views


app_name = 'inventory'

urlpatterns = [
    path('pos/inventory', views.inventory, name='inventory'),
]