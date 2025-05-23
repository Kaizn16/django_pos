from django.urls import path
from . import views

app_name = 'warehouses'


urlpatterns = [
    path('pos/warehouses', views.warehouses, name='warehouses'),
    path('pos/warehouses/add', views.add_warehouse, name='warehouse.add'),
    path('pos/warehouses/edit/<int:id>', views.edit_warehouse, name='warehouse.edit'),
    path('pos/warehouses/edit/<int:id>/update', views.update_warehouse, name='warehouse.update'),
    path('pos/warehouses/delete/<int:id>', views.delete_warehouse, name='warehouse.delete'),
    path('api/warehouses', views.fetch_warehouses, name='warehouse.fetch')
]