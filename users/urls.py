from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('pos/users', views.users, name='users'),
    path('pos/users/add', views.add_user, name='users.add'),
    path('pos/users/edit/<int:id>', views.edit_user, name='users.edit'),
    path('pos/users/delete', views.delete_user, name='users.delete'),
]