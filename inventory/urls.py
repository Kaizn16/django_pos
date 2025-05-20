from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('pos/inventory', views.inventory, name='inventory'),
    path('pos/inventory/stocks/add', views.add_product_stock, name='inventory.add_product_stock'),
    path('pos/inventory/stocks/product/<int:id>/adjust-stock', views.adjust_stock, name='inventory.adjust_stock'),
    path('pos/inventory/stocks/<int:id>/logs', views.stock_logs, name='inventory.stock_logs'),

    path('api/stocks', views.fetch_stocks, name='inventory.fetch_stocks'),
]