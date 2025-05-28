from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from django.http import JsonResponse
from django.db.models import Q
from apps.products.models import Product, Category
from apps.inventory.models import Stock
from .models import Shift, Cart, CartItem, Discount, Transaction, TransactionItem
# Create your views here.

@login_required
@role_required('cashier')
def sales(request):

    categories = Category.objects.all()

    data = {
        'categories': categories
    }

    return render(request, 'pages/sales/index.html', data)


@login_required
def fetch_products(request):
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()

    products = Product.objects.all()

    if search_query:
        products = products.filter(product_name__icontains=search_query)

    if category_filter and category_filter != 'all':
        products = products.filter(category__category_id__iexact=category_filter)

    products = products[:15]  # Limit to first 15 products

    data = []
    for product in products:
        stock = Stock.objects.filter(product_id=product.id).first()
        data.append({
            'id': product.id,
            'product_name': product.product_name,
            'category': product.category.category_name,
            'price': float(product.selling_price),
            'stock': stock.quantity if stock else 0,
            'max_stock': stock.max_quantity if stock else 0,
            'image': product.product_image.url if product.product_image else None,
        })

    return JsonResponse(data, safe=False)

def add_to_cart(request):
    pass