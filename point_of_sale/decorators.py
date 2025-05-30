# Custom role based middleware, using this middleware will limit the people who can acccess the module you want.
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect

def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = getattr(request.user.role, 'role_type', None)
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            if user_role == 'cashier':
                return redirect('sales:sales')
            
            messages.error(request, "You do not have permission to access this page.!")
            return redirect(request.META.get('HTTP_REFERER', 'login:dashboard'))
        return _wrapped_view
    return decorator