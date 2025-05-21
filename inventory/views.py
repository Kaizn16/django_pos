from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from .models import Product, Stock, StockLog
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import transaction
# Create your views here.

@login_required
@role_required('administrator', 'manager')
def inventory(request):
    return render(request, 'pages/inventory/index.html')


@login_required
@role_required('administrator', 'manager')
def add_product_stock(request):
    products = Product.objects.all()

    data = {
        'products': products
    }

    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity'))
            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than zero.')
                return render(request, 'pages/inventory/product_stock_form.html', data)

            product = get_object_or_404(Product, pk=product_id)

            with transaction.atomic():
                stock, created = Stock.objects.get_or_create(product=product)

                StockLog.objects.create(
                    stock=stock,
                    change=quantity,
                    type='in',
                    reason='Initial stock added' if created else 'Product stock added'
                )

            messages.success(request, f'Stock for {product.product_name} updated successfully.')
            return redirect('inventory:inventory')

        except ValueError:
            messages.error(request, 'Quantity must be a valid number.')
            return render(request, 'pages/inventory/product_stock_form.html', data)

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'pages/inventory/product_stock_form.html', data)

    return render(request, 'pages/inventory/product_stock_form.html', data)

def fetch_stocks(request):
    try:
        search_query = request.GET.get('search', '')
        page_number = request.GET.get('page', 1)
        per_page = 10

        stocks = Stock.objects.select_related('product').all()

        if search_query:
            stocks = stocks.filter(
                Q(product__product_name__icontains=search_query)
            )

        paginator = Paginator(stocks, per_page)
        page = paginator.get_page(page_number)

        data = []
        for stock in page:
            data.append({
                'stock_id': stock.id,
                'quantity': stock.quantity,
                'max_quantity': stock.max_quantity,
                'product_id': stock.product_id,
                'product_name': stock.product.product_name,
            })

        return JsonResponse({
            'stocks': data,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'num_pages': paginator.num_pages,
            'current_page': page.number,
        })

    except Exception as e:
        return JsonResponse({'error': 'An error occurred while fetching stocks.'}, status=500)

@login_required
@role_required('administrator', 'manager')
def adjust_stock(request, id=None):
    stock = Stock.objects.select_related('product').filter(pk=id).first()

    if not stock:
        messages.error(request, "Product stock not found!")
        return redirect('inventory:inventory')

    data = {
        'stock': stock,
    }

    if request.method == "POST":
        try:
            change = int(request.POST.get('change'))
            type_ = request.POST.get('type')
            reason = request.POST.get('reason', '')

            # Normalize change value based on type
            if type_ == 'out':
                change = -abs(change)
                if stock.quantity + change < 0:
                    messages.error(request, "Insufficient stock for this operation.")
                    return render(request, 'pages/inventory/adjust_stock_form.html', data)
            else:
                change = abs(change)

            with transaction.atomic(): # we use transaction here to ensure data consistency
                # Update the stock quantity
                stock.quantity += change
                stock.save()

                # Log the stock change
                StockLog.objects.create(
                    stock=stock,
                    change=change,
                    type=type_,
                    reason=reason,
                    reference_type='adjustment',
                    reference_id=None
                )

            messages.success(request, "Stock updated successfully.")
            return redirect('inventory:inventory')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'pages/inventory/adjust_stock_form.html', data)

    return render(request, 'pages/inventory/adjust_stock_form.html', data)


@login_required
@role_required('administrator', 'manager')
def stock_logs(request, id=None):
    stockLog = StockLog.objects.filter(stock_id=id).first()

    if not stockLog:
        messages.error(request, "There's no stock log for that product yet!")
        return redirect('inventory:inventory')

    stock = stockLog.stock
    product = stock.product

    stockLogs = StockLog.objects.filter(stock_id=stock.id).order_by('-created_at')

    paginator = Paginator(stockLogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'stockLog': stockLog,
        'product': product,
        'page_obj': page_obj,
    }

    return render(request, 'pages/inventory/stock_logs.html', data)