from django.test import TestCase
from django.urls import reverse
from api.models import *

class Shopping(TestCase):
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

    # Product search test
    def test_product_search(self):
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=100,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller
        )

        response = self.client.get(reverse("product") + "?q=testproduct")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testproduct")

    # Product sorting test
    def test_sort_products(self):
        product1 = StoreStock.objects.create(
            name="product1",
            stock_quantity=100,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller,
            is_approved=True
        )

        product2 = StoreStock.objects.create(
            name="product2",
            stock_quantity=10,
            price=10.00,
            description="test description",
            image=None,
            seller=self.seller,
            is_approved=True
        )

        response = self.client.get(reverse("product"), {"sort": "price", "order": "asc"})
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        self.assertLess(products[0].price, products[1].price)

        response = self.client.get(reverse("product"), {"sort": "price", "order": "desc"})
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        self.assertGreater(products[0].price, products[1].price)

        response = self.client.get(reverse("product"), {"sort": "name", "order": "asc"})
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        self.assertLess(products[0].name, products[1].name)

        response = self.client.get(reverse("product"), {"sort": "name", "order": "desc"})
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        self.assertGreater(products[0].name, products[1].name)

        response = self.client.get(reverse("product"), {"sort": "stock_quantity", "order": "asc"})
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        self.assertLess(products[0].stock_quantity, products[1].stock_quantity)

        response = self.client.get(reverse("product"), {"sort": "stock_quantity", "order": "desc"})
        self.assertEqual(response.status_code, 200)
        products = response.context["products"]
        self.assertGreater(products[0].stock_quantity, products[1].stock_quantity)




