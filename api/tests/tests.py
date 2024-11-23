from django.test import TestCase
from django.urls import reverse
from api.models import *

class TestViews(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username="buyer1",
            email="buyer@gmail.com",
            password="password",
            account_type="buyer"
        )

        self.seller = User.objects.create_user(
            username="seller1",
            email="seller@gmail.com",
            password="password",
            account_type="seller",
            is_staff=True
        )

        self.admin = User.objects.create_user(
            username="admin1",
            email="admin@gmail.com",
            password="password",
            account_type="admin",
            is_superuser=True
        )

        self.product = StoreStock.objects.create(
            name="product1",
            description="product description",
            price=10.00,
            stock_quantity=10,
            image=None,
            seller=self.seller,
        )

        self.cart = Cart.objects.create(
            user=self.buyer,
            quantity=1
        )

        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )


    def test_approve_product(self):
        self.client.login(username="admin1", password="password")
        response = self.client.post(reverse("approve_product", args=[self.product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin"))
        self.assertTrue(StoreStock.objects.get(id=self.product.id).is_approved)

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product approved successfully!")

    def test_reject_product(self):
        self.client.login(username="admin1", password="password")
        response = self.client.post(reverse("reject_product", args=[self.product.id]))

        self.assertFalse(StoreStock.objects.filter(id=self.product.id).exists())

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("admin"))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Product rejected!")

    def test_payment_process(self):
        self.client.login(username="buyer1", password="password")
        response = self.client.post(reverse("process_payment"))

        self.product.refresh_from_db()
        self.cart.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cart_html"))
        self.assertEqual(self.product.stock_quantity, 8)
        self.assertFalse(self.cart.items.exists())

        order = Order.objects.filter(user=self.buyer).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, 20)
        self.assertEqual(order.status, "pending")

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Payment processed successfully! Your order has been placed.")