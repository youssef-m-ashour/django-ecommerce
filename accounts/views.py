from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import RegistrationForm, EmailAuthenticationForm
from orders.models import Order


def register_view(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect('shop:product_list')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Only redirect to URLs on this same site (prevents open redirects).
                next_url = request.GET.get('next')
                if next_url and url_has_allowed_host_and_scheme(
                    next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
                ):
                    return redirect(next_url)
                return redirect('shop:product_list')
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = EmailAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('shop:product_list')


@login_required
def profile_view(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')[:5]
    return render(request, 'accounts/profile.html', {'orders': orders})
