from django.test import TestCase
from django.urls import reverse
from api.models import *

class AdminTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admintest",
            password="password",
            email="admin@gmail.com",
            account_type="admin"
        )

    # LA.1 Admin tries to make account
    # Admin cannot make account. It is only made through the shell

    # LA.2 Admin tries to log in
    def test_admin_login(self):
        response = self.client.post(reverse('login'), {
            "username": "admintest",
            "password": "password",
            "account_type": "admin"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    # LA.3 Admin tries to change information
    def test_admin_change_info(self):
        self.client.login(username="admintest", password="password")
        response = self.client.post(reverse('update_profile'), {
            "username": "newadmintest",
            "email": "newadmin@gmail.com"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_profile"))

        self.assertTrue(User.objects.filter(username="newadmintest").exists())
        self.assertTrue(User.objects.filter(email="newadmin@gmail.com").exists())

    # LA.4 Admin tries to do admin commands
    def test_admin_admin_commands(self):
        self.client.login(username="admintest", password="password")
        response = self.client.get(reverse('admin'))
        self.assertEqual(response.status_code, 302)

    # LA.5 Admin tries to delete account
    def test_admin_delete_account(self):
        self.client.login(username="admintest", password="password")
        response = self.client.post(reverse('delete_account'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(User.objects.filter(username="admintest").exists())


    # IA.1 Add item to inventory
    def test_admin_add_item(self):
        self.client.login(username="admintest", password="password")
        response = self.client.post(reverse('new_product'), {
            "productname": "item1",
            "productquantity": 10,
            "productprice": 10,
            "productdesc": "item1 description",
            "productimage": "product_images/placeholder.png",
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(StoreStock.objects.filter(name="item1").exists())

    # IA.2 Change Stock
    def test_admin_change_stock(self):
        self.client.login(username="admintest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.admin,
        )

        response = self.client.post(reverse('update_storestock', args=[product.id]), {
            "productquantity": 20
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(StoreStock.objects.get(id=product.id).stock_quantity, 20)

    # IA.3 Change Price
    def test_admin_change_price(self):
        self.client.login(username="admintest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.admin,
        )

        response = self.client.post(reverse('update_storestock', args=[product.id]), {
            "productprice": 30
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(StoreStock.objects.get(id=product.id).price, 30.00)

    # IA.4 Change Name
    def test_admin_change_name(self):
        self.client.login(username="admintest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.admin,
        )

        response = self.client.post(reverse('update_storestock', args=[product.id]), {
            "productname": "newname"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(StoreStock.objects.get(id=product.id).name, "newname")

    # IA.5 Remove item from inventory
    def test_admin_remove_item(self):
        self.client.login(username="admintest", password="password")
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.admin,
        )

        response = self.client.post(reverse('remove_from_storestock', args=[product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(StoreStock.objects.filter(name="testproduct").exists())