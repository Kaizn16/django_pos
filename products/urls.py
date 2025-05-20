from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('pos/products', views.products, name='products'),
    path('pos/products/add', views.add_product, name='product.add'),
    path('pos/products/edit/<int:id>', views.edit_product, name='product.edit'),
    path('pos/products/update/<int:id>', views.update_product, name='product.update'),
    path('pos/products/delete/<int:id>', views.delete_product, name='product.delete'),

    path('pos/products/categories', views.categories, name='categories'),
    path('pos/products/categories/add', views.add_category, name='category.add'),
    path('pos/products/categories/edit/<int:id>', views.edit_category, name='category.edit'),
    path('pos/products/categories/update/<int:id>', views.update_category, name='category.update'),
    path('pos/products/categories/delete/<int:id>', views.delete_category, name='category.delete'),

    path('api/products', views.fetch_products, name='products.fetch_products'),
    path('api/products/categories', views.fetch_categories, name='products.categories.fetch_categories'),
]