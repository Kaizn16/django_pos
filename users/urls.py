from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('pos/users', views.users, name='users'),
    path('pos/users/add', views.add_user, name='users.add'),
    path('pos/users/edit/<int:id>', views.edit_user, name='users.edit'),
    path('pos/users/update/<int:id>', views.update_user, name='users.update'),
    path('pos/users/delete/<int:id>', views.delete_user, name='users.delete'),
    path('api/users', views.fetch_users, name='users.fetch_users'),
    path('pos/user/my-profile/<int:id>', views.my_profile, name='users.myprofile'),
    path('pos/user/change-password/<int:id>', views.change_password, name='users.changepassword')
]