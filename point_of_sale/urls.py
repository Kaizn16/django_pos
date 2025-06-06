"""
URL configuration for point_of_sale project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")), # auto reload page development
    path('', include('apps.login.urls', namespace='login')),
    path('', include('apps.users.urls', namespace='users')),
    path('', include('apps.sales.urls', namespace='sales')),
    path('', include('apps.products.urls', namespace='products')),
    path('', include('apps.inventory.urls', namespace='inventory')),
    path('', include('apps.warehouses.urls', namespace='warehouses')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)