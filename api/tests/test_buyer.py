from django.test import TestCase
from django.urls import reverse
from api.models import *

class BuyerTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            username="buyertest",
            password="password",
            email="buyer@gmail.com",
            account_type="buyer"
        )

        self.seller = User.objects.create_user(
            username="sellertest",
            password="password",
            email="seller@gmail.com",
            account_type="seller"
        )

    # LB.1 Buyer tries to make account
    def test_buyer_register(self):
        response = self.client.post(reverse('register'), {
            "username": "buyertest",
            "password1": "password",
            "password2": "password",
            "email": "buyer@gmail.com",
            "account_type": "buyer"
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username="buyertest").exists())

    # LB.2 Buyer tries to log in
    def test_buyer_login(self):
        response = self.client.post(reverse('login'), {
            "username": "buyertest",
            "password": "password",
            "account_type": "buyer"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    # LB.3 Buyer tries to change information
    def test_buyer_change_info(self):
        self.client.login(username="buyertest", password="password")
        response = self.client.post(reverse('update_profile'), {
            "username": "newbuyertest",
            "email": "newbuyer@gmail.com"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_profile"))

        self.assertTrue(User.objects.filter(username="newbuyertest").exists())
        self.assertTrue(User.objects.filter(email="newbuyer@gmail.com").exists())

    # LB.4 Buyer tries to do admin commands
    def test_buyer_admin_commands(self):
        self.client.login(username="buyertest", password="password")
        response = self.client.get(reverse('admin'))

        self.assertEqual(response.status_code, 302)
        expected_url = f"{reverse('home')}?next={reverse('admin')}"
        self.assertRedirects(response, expected_url)

    # LB.5 Buyer tries to delete account
    def test_buyer_delete_account(self):
        self.client.login(username="buyertest", password="password")
        response = self.client.post(reverse('delete_account'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

        self.assertFalse(User.objects.filter(username="buyertest").exists())

    # SB.1 Buyer tries to Add to Cart
    def test_buyer_add_to_cart(self):
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller,
            is_approved=True
        )

        self.client.login(username="buyertest", password="password")
        response = self.client.get(reverse("add_to_cart", args=[product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cart"))

        cart = Cart.objects.filter(user=self.buyer).first()
        self.assertIsNotNone(cart, "Cart was not created for the buyer.")

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        self.assertIsNotNone(cart_item, "CartItem was not created for the product.")
        self.assertEqual(cart_item.quantity, 1, "The quantity of the product in the cart should be 1.")

    # SB.2 Buyer tries to Remove from Cart
    def test_buyer_remove_from_cart(self):
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=10,
            price=20.00,
            description="test description",
            image=None,
            seller=self.seller
        )

        cart = Cart.objects.create(user=self.buyer)
        CartItem.objects.create(cart=cart, product=product, quantity=1)

        self.client.login(username="buyertest", password="password")
        response = self.client.get(reverse("remove_from_cart", args=[product.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("cart"))

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        self.assertIsNone(cart_item, "CartItem was not removed from the cart.")

    # SB.3 Buyer tries to Search for Item
    def test_buyer_search_item(self):
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

    # SB.4 Buyer tries to Sort Inventory
    def test_buyer_sort_inventory(self):
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

    # SB.5 Buyer tries to Buy Out of Stock Item
    def test_buyer_buy_out_of_stock_item(self):
        product = StoreStock.objects.create(
            name="testproduct",
            stock_quantity=0,
            price=20.00,
            description="test description",
            image="product_images/placeholder.png",
            seller=self.seller,
            is_approved=True
        )

        self.client.login(username="buyertest", password="password")
        response = self.client.get(reverse("product_detail", args=[product.id]))
        self.assertContains(response, "Out of Stock")
        self.assertNotContains(response, "Add to Cart")