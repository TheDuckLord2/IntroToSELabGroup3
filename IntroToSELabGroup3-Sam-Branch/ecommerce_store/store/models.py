from django.db import models
from django.contrib.auth.models import AbstractUser

class StoreStock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()

    class Meta:
        db_table = 'StoreStock'

    def __str__(self):
        return self.name

class User(AbstractUser):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    #username = models.CharField(max_length=255, unique=True)
    #password = models.CharField(max_length=255)
    #email = models.EmailField(unique=True)
    account_type = models.CharField(max_length=255, choices=USER_TYPES)

    # Override the related_name for groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name= 'custom_user_permissions',
        blank=True,
    )

    class Meta:
        db_table = 'User'

    def __str__(self):
        return self.username

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(StoreStock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'Cart'

    def __str__(self):
        return f"Cart of {self.user.username}"

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

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(StoreStock, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'OrderDetails'

    def __str__(self):
        return f"Order Details {self.id} for Order {self.order.id}"
