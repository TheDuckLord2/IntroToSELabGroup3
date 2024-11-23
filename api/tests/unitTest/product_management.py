from django.test import TestCase
from django.urls import reverse
from api.models import *

class ProductManagement(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            username="testseller",
            email="testseller@gmail.com",
            password="password",
            account_type="seller"
        )

        self.admin = User.objects.create_user(
            username="testadmin",
            email="testadmin@gmail.com",
            password="password",
            account_type="admin"
        )

    # Product creation test
    def test_product_creation(self):
        self.client.login(username=self.seller.username, password="password")
        response = self.client.post(reverse('new_product'), {
            "productname": "Test Product",
            "productquantity": 10,
            "productprice": 20.00,
            "productdesc": "Test description",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(StoreStock.objects.filter(name="Test Product").exists())

    # Product approval test
    def test_product_approval(self):
        product = StoreStock.objects.create(
            name="Unapproved Product",
            stock_quantity=5,
            price=50.00,
            seller=self.seller,
            is_approved=False
        )

        self.client.login(username=self.admin.username, password="password")
        response = self.client.post(reverse('approve_product', args=[product.id]))
        product.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(product.is_approved)

    # Reject product test
    def test_reject_product(self):
        product = StoreStock.objects.create(
            name="Product to Reject",
            stock_quantity=5,
            price=50.00,
            image=None,
            seller=self.seller
        )

        self.client.login(username=self.admin.username, password="password")
        response = self.client.post(reverse('reject_product', args=[product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StoreStock.objects.filter(id=product.id).exists())

