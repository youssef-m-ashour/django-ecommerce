from decimal import Decimal
from django.conf import settings
from shop.models import Product

CART_SESSION_KEY = 'cart'


class Cart:
    """
    A session-based shopping cart. Stored as:
    { "<product_id>": {"quantity": int} }
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1, replace=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if replace:
            new_quantity = quantity
        else:
            new_quantity = self.cart[product_id]['quantity'] + quantity

        # Never allow more than available stock.
        new_quantity = max(0, min(new_quantity, product.stock))
        self.cart[product_id]['quantity'] = new_quantity
        self.save()
        return new_quantity

    def decrease(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                del self.cart[product_id]
            self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        products_map = {str(p.id): p for p in products}

        for product_id, item in self.cart.items():
            product = products_map.get(product_id)
            if not product:
                continue
            quantity = item['quantity']
            yield {
                'product': product,
                'quantity': quantity,
                'subtotal': product.price * quantity,
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self:
            total += item['subtotal']
        return total

    def get_items(self):
        return list(self)
