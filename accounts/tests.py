from django.test import TestCase
from django.urls import reverse

from .models import CustomUser


class AuthTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='user@example.com', email='user@example.com',
            password='StrongPass123!', first_name='Test', last_name='User',
            mobile_phone='01012345678',
        )

    def login(self, next_url=None):
        url = reverse('accounts:login')
        if next_url:
            url += f'?next={next_url}'
        return self.client.post(
            url, {'email': 'user@example.com', 'password': 'StrongPass123!'}
        )

    def test_login_redirects_to_safe_next_url(self):
        response = self.login(next_url='/cart/')
        self.assertRedirects(response, '/cart/', fetch_redirect_response=False)

    def test_login_ignores_external_next_url(self):
        response = self.login(next_url='https://evil.example.com/')
        self.assertRedirects(
            response, reverse('shop:product_list'), fetch_redirect_response=False
        )

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('accounts:logout')).status_code, 405)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_with_post(self):
        self.client.force_login(self.user)
        self.client.post(reverse('accounts:logout'))
        self.assertNotIn('_auth_user_id', self.client.session)
