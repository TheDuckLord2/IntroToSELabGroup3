from django.test import TestCase
from django.urls import reverse
from api.models import *

class TestModels(TestCase):
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
            seller=self.seller
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

        self.order = Order.objects.create(
            user=self.buyer,
            total_price=20.00,
            status="pending"
        )

        self.order_detail = OrderDetails.objects.create(
            order=self.order,
            item=self.product,
            quantity=2,
            price=20.00
        )

        self.shipping_info = ShippingInformation.objects.create(
            order=self.order,
            recipient_name="buyer1",
            address="buyer's address",
            city="buyer's city",
            state="GA",
            postal_code="12345",
            country="USA",
            phone_number="123-456-7890"
        )

    def test_user_model(self):
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(self.buyer.account_type, "buyer")
        self.assertTrue(self.seller.is_staff)
        self.assertTrue(self.admin.is_superuser)

    def test_store_stock_model(self):
        self.assertEqual(StoreStock.objects.count(), 1)
        self.assertEqual(self.product.name, "product1")
        self.assertEqual(self.product.price, 10.00)
        self.assertEqual(self.product.stock_quantity, 10)
        self.assertEqual(self.product.seller, self.seller)

    def test_cart_model(self):
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(self.cart.user, self.buyer)
        self.assertEqual(self.cart.quantity, 1)

    def test_cart_item_model(self):
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.total_price(), 20.00)

    def test_order_model(self):
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.user, self.buyer)
        self.assertEqual(self.order.total_price, 20.00)
        self.assertEqual(self.order.status, "pending")

    def test_order_details_model(self):
        self.assertEqual(OrderDetails.objects.count(), 1)
        self.assertEqual(self.order_detail.order, self.order)
        self.assertEqual(self.order_detail.item, self.product)
        self.assertEqual(self.order_detail.quantity, 2)
        self.assertEqual(self.order_detail.price, 20.00)

    def test_shipping_information_model(self):
        self.assertEqual(ShippingInformation.objects.count(), 1)
        self.assertEqual(self.shipping_info.order, self.order)
        self.assertEqual(self.shipping_info.recipient_name, "buyer1")
        self.assertEqual(self.shipping_info.address, "buyer's address")
        self.assertEqual(self.shipping_info.city, "buyer's city")
        self.assertEqual(self.shipping_info.state, "GA")
        self.assertEqual(self.shipping_info.postal_code, "12345")
        self.assertEqual(self.shipping_info.country, "USA")
        self.assertEqual(self.shipping_info.phone_number, "123-456-7890")