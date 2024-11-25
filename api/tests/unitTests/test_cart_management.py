from django.test import TestCase
from django.urls import reverse
from api.models import *

class CartManagement(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            username="testseller",
            email="testseller@gmail.com",
            password="password",
            account_type="seller"
        )

        self.buyer = User.objects.create_user(
            username="testbuyer",
            email="testbuyer@gmail.com",
            password="password",
            account_type="buyer"
        )

    # Adding product to cart
    def test_add_to_cart(self):
        product = StoreStock.objects.create(
            name="Test Product",
            stock_quantity=10,
            price=20.00,
            image=None,
            seller=self.seller
        )

        cart = Cart.objects.create(user=self.buyer)
        self.client.login(username=self.buyer.username, password="password")
        response = self.client.post(reverse('add_to_cart', args=[product.id]), {"quantity": 1})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CartItem.objects.filter(cart=cart, product=product).exists())

    # Removing product from cart
    def test_remove_from_cart(self):
        product = StoreStock.objects.create(
            name="Test Product",
            stock_quantity=10,
            price=20.00,
            image=None,
            seller=self.seller
        )

        cart = Cart.objects.create(user=self.buyer)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
        self.client.login(username=self.buyer.username, password="password")
        response = self.client.post(reverse('remove_from_cart', args=[product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(cart=cart, product=product).exists())


