from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from .forms import ShippingForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('shop:product_list')

    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            items = cart.get_items()

            # Re-validate stock right before creating the order.
            for item in items:
                if item['quantity'] > item['product'].stock:
                    messages.error(
                        request,
                        f"Not enough stock for {item['product'].title}. "
                        f"Only {item['product'].stock} left."
                    )
                    return redirect('cart:cart_detail')

            with transaction.atomic():
                order = Order.objects.create(
                    customer=request.user,
                    full_name=form.cleaned_data['full_name'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    phone=form.cleaned_data['phone'],
                    total_price=cart.get_total_price(),
                )
                for item in items:
                    product = item['product']
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=item['quantity'],
                    )
                    product.stock -= item['quantity']
                    product.save(update_fields=['stock'])

            cart.clear()
            messages.success(request, "Your order has been placed successfully!")
            return redirect('orders:order_detail', order_id=order.id)
    else:
        form = ShippingForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
