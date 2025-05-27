from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView


app_name = 'login'

urlpatterns = [
    path('', views.home_view, name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('pos/dashboard', views.dashboard, name='dashboard')
]