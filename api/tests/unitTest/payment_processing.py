from django.test import TestCase
from django.urls import reverse
from api.models import *

class PaymentProcessing(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username="testbuyer",
            email="testbuyer@gmail.com",
            password="password",
            account_type="buyer"
        )

        self.seller = User.objects.create_user(
            username="testseller",
            email="testseller@gmail.com",
            password="password",
            account_type="seller"
        )

    # Payment processing test
    def test_process_payment(self):
        product = StoreStock.objects.create(
            name="Product",
            stock_quantity=5,
            price=50.00,
            image=None,
            seller=self.seller
        )

        cart = Cart.objects.create(user=self.buyer)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        self.client.login(username=self.buyer.username, password="password")
        response = self.client.post(reverse('process_payment'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart_html'))
        product.refresh_from_db()
        self.assertEqual(product.stock_quantity, 4)
        self.assertTrue(Order.objects.filter(user=self.buyer).exists())
