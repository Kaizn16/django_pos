from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from point_of_sale.decorators import role_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render

# handle the remember me functionality
class CustomLoginView(LoginView):

    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        response = super().form_valid(form)

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(1209600)

        return response
    
    def get_success_url(self):
        return reverse_lazy('login:dashboard')


# If the user is already authenticated, and if visit back to login page, redirect back to dashboard
def home_view(request):
    if request.user.is_authenticated:
        return redirect('login:dashboard')
    return redirect('login:login')

@login_required
@role_required('administrator', 'manager')
def dashboard(request):
    
    if not request.session.get('has_seen_login_message', False):
        messages.success(request, "Login successfully!")
        request.session['has_seen_login_message'] = True

    return render(request, 'pages/dashboard.html')