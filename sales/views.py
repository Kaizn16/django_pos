from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from products.models import Product, Category
from inventory.models import Stock
from django.http import JsonResponse
# Create your views here.

@login_required
# @role_required('cashier')
def sales(request):

    categories = Category.objects.all()

    data = {
        'categories': categories
    }

    return render(request, 'pages/sales/index.html', data)


@login_required
def fetch_products(request):
    products = Product.objects.all()[:15]

    data = []
    for product in products:
        stock = Stock.objects.filter(product_id=product.id).first()
        data.append({
            'product_name': product.product_name,
            'price': product.selling_price,
            'stock': stock.quantity if stock else 0,
            'max_stock': stock.max_quantity if stock else 0,
            'image': product.product_image.url if product.product_image else None,
        })

    return JsonResponse(data, safe=False)