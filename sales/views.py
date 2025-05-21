from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
# Create your views here.

@login_required
# @role_required('cashier')
def sales(request):
    return render(request, 'pages/sales/index.html')