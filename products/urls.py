from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('pos/products', views.products, name='products'),
    path('pos/products/add', views.add_product, name='products.add'),
    path('pos/products/edit/<int:id>', views.edit_product, name='products.edit'),
    path('pos/products/update/<int:id>', views.update_product, name='products.update'),
    path('pos/products/delete/<int:id>', views.delete_product, name='products.delete'),
    path('api/products', views.fetch_products, name='products.fetch_products'),
]