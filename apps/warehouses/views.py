from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from .models import Warehouse
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction

# Create your views here.
@login_required
@role_required('administrator', 'manager')
def warehouses(request):
    return render(request, 'pages/warehouses/index.html')

@login_required
@role_required('administrator', 'manager')
def add_warehouse(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            location = request.POST.get('location')

            Warehouse.objects.create(
                name=name,
                location=location,
            )

            messages.success(request, 'Warehouse created successfully.')
            return redirect('warehouses:warehouses')

        except Exception as e:
            messages.error(request, 'An error occurred while creating the warehouse.')

        form_data = {
            'name': request.POST.get('name'),
            'location': request.POST.get('location'),
        }

        return render(request, 'pages/warehouses/warehouse_form.html', {'form_data': form_data})

    return render(request, 'pages/warehouses/warehouse_form.html')    


@login_required
@role_required('administrator', 'manager')
def edit_warehouse(request, id=None):
    try:
        warehouse = Warehouse.objects.get(pk=id)
    except Warehouse.DoesNotExist:
        messages.error(request, "Warehouse not found.")
        return redirect('warehouses:warehouse')
    
    form_data = {
        'name': warehouse.name,
        'location': warehouse.location,
        'status': warehouse.is_active,
    }

    data = {
        'warehouse': warehouse,
        'form_data': form_data,
    }

    return render(request, 'pages/warehouses/warehouse_form.html', data)

@login_required
def update_warehouse(request, id=None):
    warehouse = get_object_or_404(Warehouse, pk=id)
   

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        status = request.POST.get('status') == 'on'

        warehouse.name = name
        warehouse.location = location
        warehouse.is_active = status
        warehouse.save()

        messages.success(request, "Warehouse updated successfully.")
        return redirect('warehouses:warehouses')

    form_data = {
        'name': warehouse.name,
        'location': warehouse.location,
        'status': warehouse.is_active,
    }

    data = {
        'warehouse': warehouse,
        'form_data': form_data,
    }

    return render(request, 'pages/warehouses/warehouse_form.html', data)

@login_required
@role_required('administrator', 'manager')
def delete_warehouse(request, id=None):
    pass

@login_required
def fetch_warehouses(request):
    try:
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        per_page = 10

        warehouses = Warehouse.objects.all()

        if search_query:
            warehouses = warehouses.filter(
                Q(name__icontains=search_query)
            )

        paginator = Paginator(warehouses, per_page)
        page = paginator.get_page(page_number)

        data = []
        for warehouse in page:
            data.append({
                'id': warehouse.id,
                'name': warehouse.name,
                'location': warehouse.location,
                'status': warehouse.is_active
            })

        return JsonResponse({
            'warehouses': data,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'num_pages': paginator.num_pages,
            'current_page': page.number,
        })

    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching warehouse.'}, status=500)
