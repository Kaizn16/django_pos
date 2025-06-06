from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import IntegrityError
from .models import Product, Category


# Create your views here.
# Products Module

@login_required
@role_required('administrator', 'manager')
def products(request):
    return render(request, 'pages/products/index.html')

@login_required
@role_required('administrator', 'manager')
def add_product(request):
    try:
        categories = Category.objects.all()

        if request.method == 'POST':
            product_image = request.FILES.get('product_image')
            product_name = request.POST.get('product_name')
            category_id = request.POST.get('category')
            description = request.POST.get('description')
            selling_price = request.POST.get('selling_price')
            buying_price = request.POST.get('buying_price')
            low_stock_threshold = request.POST.get('low_stock_threshold')
            sku = request.POST.get('sku')
            barcode = request.POST.get('barcode')

            # Pre-fill form data for redisplay if something went wrong
            form_data = {
                'product_name': product_name,
                'category': category_id,
                'description': description,
                'selling_price': selling_price,
                'buying_price': buying_price,
                'low_stock_threshold': low_stock_threshold,
                'sku': sku,
                'barcode': barcode,
            }

            validations = False

            if Product.objects.filter(product_name=product_name).exists():
                messages.error(request, "Product already exists!")
                validations = True
  

            if not validations:
                product_data = {
                    'product_name': product_name,
                    'category': Category.objects.get(pk=category_id),
                    'description': description,
                    'selling_price': selling_price,
                    'buying_price': buying_price,
                    'low_stock_threshold': low_stock_threshold,
                    'sku': sku,
                    'barcode': barcode,
                }

                if product_image:
                    product_data['product_image'] = product_image
                
                if description:
                    product_data['description'] = description
                
                if sku:
                    product_data['sku'] = sku

                if barcode:
                    product_data['barcode'] = barcode

                Product.objects.create(**product_data)
                messages.success(request, "Product successfully created!")
                return redirect('products:products')

            return render(request, 'pages/products/product_form.html', {
                'categories': categories,
                'product': None,
                'form_data': form_data
            })


        return render(request, 'pages/products/product_form.html', {
            'categories': categories
        })

    except Exception as e:
        return HttpResponse(f'Error occurred during adding product. {e}')


@login_required
@role_required('administrator', 'manager')
def edit_product(request, id=None):
    categories = Category.objects.all()

    try:
        product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('products:products')

    form_data = {
        'product_name': product.product_name,
        'category': str(product.category.category_id),
        'description': product.description,
        'selling_price': product.selling_price,
        'buying_price': product.buying_price,
        'low_stock_threshold': product.low_stock_threshold,
        'sku': product.sku,
        'barcode': product.barcode,
        'status': product.status,
    }

    data = {
        'categories': categories,
        'product': product,
        'form_data': form_data,
    }

    return render(request, 'pages/products/product_form.html', data)

@login_required
@role_required('administrator', 'manager')
def update_product(request, id=None):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        try:
            product_name = request.POST.get('product_name')
            category_id = request.POST.get('category')
            description = request.POST.get('description')
            selling_price = request.POST.get('selling_price')
            buying_price = request.POST.get('buying_price')
            low_stock_threshold = request.POST.get('low_stock_threshold')
            sku = request.POST.get('sku')
            barcode = request.POST.get('barcode')
            product_image = request.FILES.get('product_image')
            status = request.POST.get('status') == 'on'  

            product.product_name = product_name
            product.category = Category.objects.get(pk=category_id)
            product.selling_price = selling_price
            product.buying_price = buying_price
            product.low_stock_threshold = low_stock_threshold
            product.status = status

            if product_name != product.product_name:
                product.product_name = product_name
            
            if description:
                product.description = description

            if sku:
                product.sku = sku
        
            if barcode:
                product.barcode = barcode

            if product_image:
                product.product_image = product_image

            product.save()
            messages.success(request, "Product updated successfully.")
            return redirect('products:products')

        except IntegrityError as e:
            messages.error(request, "Product name already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    form_data = {
        'product_name': product.product_name,
        'category': str(product.category),
        'username': product.username,
        'email': product.email,
    }

    categories = Category.objects.all()
    return render(request, 'pages/products/product_form.html', {
        'product': product,
        'form_data': form_data,
        'categories': categories
    })

@login_required
@role_required('administrator', 'manager')
def delete_product(request, id=None):
    if request.method == 'POST':
        
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('products:products')

        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('products:products')

    messages.error(request, "Invalid request method.")
    return redirect('products:products')

def fetch_products(request):
    try:
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        per_page = 10

        products = Product.objects.all()

        if search_query:
            products = products.filter(
                Q(product_name__icontains=search_query)
            )

        paginator = Paginator(products, per_page)
        page = paginator.get_page(page_number)

        data = []
        for product in page:
            data.append({
                'id': product.id,
                'product_image': product.product_image.url if product.product_image else None,
                'product_name': product.product_name,
                'category': getattr(product.category, 'category_name', 'N/A'),
                'selling_price': product.selling_price,
                'buying_price': product.buying_price,
                'low_stock_threshold': product.low_stock_threshold,
                'status': product.status,
            })

        return JsonResponse({
            'products': data,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'num_pages': paginator.num_pages,
            'current_page': page.number,
        })
    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching products.'}, status=500)
    


# Categories Module

@login_required
@role_required('administrator', 'manager')
def categories(request):
    try:
        return render(request, 'pages/products/categories/index.html')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}") 

@login_required
@role_required('administrator', 'manager')
def add_category(request):
    try:
        if request.method == 'POST':
            category_name = request.POST.get('category_name')

            # Pre-fill form data for redisplay if something went wrong
            form_data = {'category_name': category_name}

            validations = False

            if Category.objects.filter(category_name=category_name).exists():
                messages.error(request, "Category already exists!")
                validations = True
  
            if not validations:
                category_data = {'category_name': category_name,}

                Category.objects.create(**category_data)
                messages.success(request, "Category successfully created!")
                return redirect('products:categories')

            return render(request, 'pages/products/categories/category_form.html', {
                'category': None,
                'form_data': form_data
            })

        return render(request, 'pages/products/categories/category_form.html')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}") 


@login_required
@role_required('administrator', 'manager')
def edit_category(request, id=None):
    try:
        category = Category.objects.get(pk=id)
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('products:products')

    form_data = {'category_name': category.category_name,}

    data = {
        'category': category,
        'form_data': form_data,
    }

    return render(request, 'pages/products/categories/category_form.html', data)


@login_required
@role_required('administrator', 'manager')
def update_category(request, id=None):
    category = get_object_or_404(Category, pk=id)
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category_name')
    
            if category_name != category.category_name:
                category.category_name = category_name
            
            category.save()
            messages.success(request, "Category updated successfully.")
            return redirect('products:categories')

        except IntegrityError as e:
            messages.error(request, "Category name already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    form_data = {'category_name': category.category_name}

    return render(request, 'pages/products/categories/category_form.html', {
        'category': category,
        'form_data': form_data,
    })

@login_required
@role_required('administrator', 'manager')
def delete_category(request, id=None):
    if request.method == 'POST':
        
        try:
            category = Category.objects.get(pk=id)
        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
            return redirect('products:categories')

        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('products:categories')

    messages.error(request, "Invalid request method.")
    return redirect('products:categories')

def fetch_categories(request):
    try:
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        per_page = 10

        categories = Category.objects.all()

        if search_query:
            categories = categories.filter(
                Q(category_name__icontains=search_query)
            )

        paginator = Paginator(categories, per_page)
        page = paginator.get_page(page_number)

        data = []
        for category in page:
            data.append({
                'category_id': category.category_id,
                'category_name': category.category_name,
            })

        return JsonResponse({
            'categories': data,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'num_pages': paginator.num_pages,
            'current_page': page.number,
        })

    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching categories.'}, status=500)