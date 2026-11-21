from django.test import TestCase
from django.urls import reverse

from shop.models import Category, Product


class CartViewsTests(TestCase):
    def setUp(self):
        category = Category.objects.create(name='Books', slug='books')
        self.product = Product.objects.create(
            category=category, title='Test Book', slug='test-book',
            description='A book', price=100, stock=5,
        )

    def test_cart_changes_require_post(self):
        urls = [
            reverse('cart:cart_add', args=[self.product.id]),
            reverse('cart:cart_increase', args=[self.product.id]),
            reverse('cart:cart_decrease', args=[self.product.id]),
            reverse('cart:cart_remove', args=[self.product.id]),
            reverse('cart:cart_clear'),
        ]
        for url in urls:
            self.assertEqual(self.client.get(url).status_code, 405, url)

    def test_add_to_cart_with_post(self):
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]), {'quantity': 2}
        )
        self.assertRedirects(response, reverse('cart:cart_detail'))
        self.assertEqual(self.client.session['cart'][str(self.product.id)]['quantity'], 2)

    def test_add_to_cart_ignores_external_next_url(self):
        response = self.client.post(
            reverse('cart:cart_add', args=[self.product.id]),
            {'quantity': 1, 'next': 'https://evil.example.com/'},
        )
        self.assertRedirects(response, reverse('cart:cart_detail'))
