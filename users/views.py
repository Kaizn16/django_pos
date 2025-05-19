from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def users(request):
    return render(request, 'pages/users/index.html')

@login_required
def add_user(request):
    return render(request, 'pages/users/add_user.html')

@login_required
def edit_user(request):
    pass

@login_required
def delete_user(request):
    pass