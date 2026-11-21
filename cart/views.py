from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from shop.models import Product
from .cart import Cart
from .forms import AddToCartForm


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)

    form = AddToCartForm(request.POST)
    quantity = form.cleaned_data['quantity'] if form.is_valid() else 1

    if product.stock <= 0:
        messages.error(request, f"{product.title} is out of stock.")
    else:
        new_qty = cart.add(product=product, quantity=quantity)
        if new_qty < quantity:
            messages.warning(
                request,
                f"Only {product.stock} unit(s) of {product.title} are available in stock."
            )
        else:
            messages.success(request, f"{product.title} added to your cart.")

    # Only redirect to URLs on this same site (prevents open redirects).
    next_url = request.POST.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(next_url)
    return redirect('cart:cart_detail')


@require_POST
def cart_increase(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('cart:cart_detail')


@require_POST
def cart_decrease(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrease(product=product)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f"{product.title} removed from cart.")
    return redirect('cart:cart_detail')


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Your cart has been cleared.")
    return redirect('cart:cart_detail')
