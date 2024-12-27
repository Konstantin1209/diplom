from django.test import TestCase

from django.test import TestCase
from django.urls import reverse

class BasketTests(TestCase):
    def setUp(self):
        pass

    def test_cookie_handling(self):

        self.client.cookies['cart'] = '{"1": {"2": 3}}' 
        response = self.client.get(reverse('cart-list'))  
        self.assertEqual(response.status_code, 200)
        self.assertIn('cart', self.client.cookies)
        self.assertEqual(self.client.cookies['cart'].value, '{"1": {"2": 3}}')

