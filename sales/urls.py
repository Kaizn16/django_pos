from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    path('pos/sales', views.sales, name='sales'),
    path('api/sales/products', views.fetch_products, name='sales.fetch_products'),
    path('pos/sales', views.add_to_cart, name='sales.add_to_cart'),
]