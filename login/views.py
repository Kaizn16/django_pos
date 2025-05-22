from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from django.contrib import messages

@login_required
@role_required('administrator', 'manager')
def dashboard(request):
    
    if not request.session.get('has_seen_login_message', False):
        messages.success(request, "Login successfully!")
        request.session['has_seen_login_message'] = True

    return render(request, 'pages/dashoard.html')