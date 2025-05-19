from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import User, Role
from django.shortcuts import render, get_object_or_404
# Create your views here.

@login_required
def users(request):
    try:
        users = User.objects.all()

        data = {
            'users': users
        }

        return render(request, 'pages/users/index.html', data)
    except Exception as e:
        return HttpResponse(f'Error occure during fetching users.')
    
@login_required
def add_user(request):
    roles = Role.objects.all()

    data = {
        'roles': roles,
        'user': None,
    }

    return render(request, 'pages/users/user_form.html', data)

@login_required
def edit_user(request, id=None):
    roles = Role.objects.all()
    user = None

    if id:
        user = get_object_or_404(User, pk=id)

    data = {
        'roles': roles,
        'user': user,
    }
    return render(request, 'pages/users/user_form.html', data)

@login_required
def delete_user(request):
    pass