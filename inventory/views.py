from django.shortcuts import render, redirect
from . import views
from django.http import HttpResponse
# Create your views here.

def inventory(request):
    return render(request, 'pages/inventory/index.html')