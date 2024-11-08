from django.db import models
from django.contrib.auth.hashers import make_password

class UserCreation(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    account_type = models.CharField(max_length=50)

    def __str__(self):
        return self.email

    #defines table
    class Meta:
        db_table = 'user'


class CreatedUser(models.Model):
    username = models.CharField(max_length=25, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'created_users'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who owns the cart
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # To track if the cart is still active or abandoned

    def __str__(self):
        return f"Cart for {self.user.username}"

    def total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        return total

    def item_count(self):
        return self.items.count()

    class Meta:
        db_table = "storestock"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('cart', 'product')

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
