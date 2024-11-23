# Imports
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

# User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, account_type=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not account_type:
            raise ValueError("The Account Type must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, account_type=account_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, account_type='admin', **extra_fields)

# User Model
class User(AbstractUser):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    account_type = models.CharField(max_length=255, choices=USER_TYPES)
    REQUIRED_FIELDS = ['email', 'account_type']
    objects = UserManager()  # Assign UserManager

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
    )

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username

# StoreStock Model
class StoreStock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    seller = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'account_type': 'seller'})
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'StoreStock'

    def __str__(self):
        return f"{self.name} by {self.seller.username}"

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #item = models.ForeignKey(StoreStock, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'Cart'

    def __str__(self):
        return f"Cart of {self.user.username}"

# CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(StoreStock, related_name='cart_items', on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'CartItem'
        unique_together = ('cart', 'product')

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Order Model
class Order(models.Model):
    STATUS = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, choices=STATUS)
    created_at = models.DateTimeField(default=now)

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# OrderDetails Model
class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(StoreStock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'OrderDetails'

    def __str__(self):
        return f"Order {self.order.id} Order Details"

# ShippingInformation Model
class ShippingInformation(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'ShippingInformation'

    def __str__(self):
        return f"Shipping for Order {self.order.id}"
