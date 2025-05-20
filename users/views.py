from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from django.http import HttpResponse
from django.contrib import messages
from .models import User, Role
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
# Create your views here.

@login_required
@role_required('administrator', 'manager') # Role Based middleware
def users(request):
    return render(request, 'pages/users/index.html')
    
@login_required
@role_required('administrator', 'manager') # Role Based middleware
def add_user(request):
    try:
        roles = Role.objects.all()
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            role_id = request.POST.get('role')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            profile = request.FILES.get('profile')

            # Pre-fill form data for redisplay
            form_data = {
                'full_name': fullName,
                'username': username,
                'email': email,
                'role': role_id,
            }

            validations = False

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                validations = True

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists!")
                validations = True

            if password != confirm_password:
                messages.error(request, "Password does not match!")
                validations = True

            if not validations:
                user_data = {
                    'full_name': fullName,
                    'username': username,
                    'email': email,
                    'role': Role.objects.get(pk=role_id),
                    'password': make_password(password),
                }

                if profile:
                    user_data['profile'] = profile

                User.objects.create(**user_data)
                messages.success(request, "User successfully created!")
                return redirect('users:users')

            return render(request, 'pages/users/user_form.html', {
                'roles': roles,
                'user': None,
                'form_data': form_data
            })

        return render(request, 'pages/users/user_form.html', {
            'roles': roles,
            'user': None
        })

    except Exception as e:
        return HttpResponse(f'Error occurred during adding user. {e}')

@login_required
@role_required('administrator', 'manager') # Role Based middleware
def edit_user(request, id=None):
    roles = Role.objects.all()

    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('users:users')

    form_data = {
        'full_name': user.full_name,
        'username': user.username,
        'email': user.email,
        'role': str(user.role.role_id),
    }

    data = {
        'roles': roles,
        'user': user,
        'form_data': form_data,
    }

    return render(request, 'pages/users/user_form.html', data)

@login_required
@role_required('administrator', 'manager') # Role Based middleware
def update_user(request, id=None):
    user = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        try:
            full_name = request.POST.get('full_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            role_id = request.POST.get('role')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            profile = request.FILES.get('profile')  

            user.full_name = full_name
            user.role = Role.objects.get(pk=role_id)

            if username != user.username:
                user.username = username

            if email != user.email:
                user.email = email

            if password:
                if password == confirm_password:
                    user.set_password(password)
                else:
                    messages.error(request, "Passwords do not match.")
                    roles = Role.objects.all()
                    form_data = {
                        'full_name': full_name,
                        'username': username,
                        'email': email,
                        'role': role_id,
                    }
                    return render(request, 'pages/users/user_form.html', {
                        'user': user,
                        'form_data': form_data,
                        'roles': roles
                    })
                
            if profile:
                user.profile = profile

            user.save()
            messages.success(request, "User updated successfully.")
            return redirect('users:users')

        except IntegrityError as e:
            messages.error(request, "Username or email already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    form_data = {
        'full_name': user.full_name,
        'username': user.username,
        'email': user.email,
        'role': str(user.role),
    }
    roles = Role.objects.all()
    return render(request, 'pages/users/user_form.html', {
        'user': user,
        'form_data': form_data,
        'roles': roles
    })

@login_required
@role_required('administrator', 'manager') # Role Based middleware
def delete_user(request, id=None):
    if request.method == 'POST':
        
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('users:users')

        user.delete()
        messages.success(request, "User deleted successfully.")
        return redirect('users:users')

    messages.error(request, "Invalid request method.")
    return redirect('users:users')

def fetch_users(request):
    try:
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        per_page = 10

        users = User.objects.exclude(id=request.user.id) #Exclude the current authenticated user when fetching.

        if search_query:
            users = users.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)
            )

        paginator = Paginator(users, per_page)
        page = paginator.get_page(page_number)

        data = []
        for user in page:
            data.append({
                'id': user.id,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '-',
                'role': getattr(user.role, 'role_type', 'N/A'),
                'profile': user.profile.url if user.profile else None,
            })

        return JsonResponse({
            'users': data,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'num_pages': paginator.num_pages,
            'current_page': page.number,
        })
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching users.'}, status=500)