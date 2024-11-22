from django.test import TestCase
from django.urls import reverse
from api.models import *

class SellerTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(
            username="sellertest",
            password="password",
            email="seller@gmail.com",
            account_type="seller"
        )

    # LS.1 Seller tries to make account
    def test_seller_register(self):
        response = self.client.post(reverse('register'), {
            "username": "newsellertest",
            "password1": "password",
            "password2": "password",
            "email": "seller@gmail.com",
            "account_type": "seller"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="newsellertest").exists())
        self.assertTrue(User.objects.get(username="newsellertest").is_staff)

    # LS.2 Seller tries to log in
    def test_seller_login(self):
        response = self.client.post(reverse('login'), {
            "username": "sellertest",
            "password": "password",
            "account_type": "seller"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    # LS.3 Seller tries to change information
    def test_seller_change_info(self):
        self.client.login(username="sellertest", password="password")
        response = self.client.post(reverse('update_profile'), {
            "username": "newsellertest",
            "email": "newseller@gmail.com",
            "account_type": "seller"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_profile"))

        self.assertTrue(User.objects.filter(username="newsellertest").exists())
        self.assertTrue(User.objects.filter(email="newseller@gmail.com").exists())

    # LS.4 Seller tries to do seller commands
    def test_seller_seller_commands(self):
        self.client.login(username="sellertest", password="password")
        response = self.client.get(reverse('manage'))
        self.assertEqual(response.status_code, 200)

    # LS.5 Seller tries to delete account
    def test_seller_delete_account(self):
        self.client.login(username="sellertest", password="password")
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        self.assertFalse(User.objects.filter(username="sellertest").exists())

    # IS.1 Add item to inventory
    def test_add_item(self):
        self.client.login(username="sellertest", password="password")
        response = self.client.post(reverse('new_product'), {
            "productname": "item1",
            "productquantity": 10,
            "productprice": 10,
            "productdesc": "item1 description",
            "productimage": "product_images/placeholder.png",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(StoreStock.objects.filter(name="item1").exists())

    # IS.2 Remove Item from Inventory
    def test_remove_item(self):
        self.client.login(username="sellertest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller,
        )

        response = self.client.post(reverse('remove_from_storestock', args=[product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StoreStock.objects.filter(name="testproduct").exists())


    # IS.3 Change Stock
    def test_change_stock(self):
        self.client.login(username="sellertest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller,
        )

        response = self.client.post(reverse('update_storestock', args=[product.id]), {
            "productquantity": 20
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(StoreStock.objects.get(id=product.id).stock_quantity, 20)

    # IS.4 Change Price
    def test_change_price(self):
        self.client.login(username="sellertest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller,
        )

        response = self.client.post(reverse('update_storestock', args=[product.id]), {
            "productprice": 30
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(StoreStock.objects.get(id=product.id).price, 30.00)

    # IS.5 Change Name
    def test_change_name(self):
        self.client.login(username="sellertest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller,
        )

        response = self.client.post(reverse('update_storestock', args=[product.id]), {
            "productname": "newtestproduct"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(StoreStock.objects.get(id=product.id).name, "newtestproduct")