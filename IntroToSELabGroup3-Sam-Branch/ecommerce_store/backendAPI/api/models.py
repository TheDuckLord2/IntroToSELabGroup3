'''from django.db import models
from django.contrib.auth.hashers import make_password



class StoreStock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    seller = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'account_type': 'seller'})


    class Meta:
        db_table = 'StoreStock'

    def __str__(self):
        return f"{self.name} by {self.seller.username}"

class UserCreation(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    #is_authenticated = models.BooleanField(default=False)
    #is_anonymous = models.BooleanField(default=False)
    id = models.CharField(max_length=5, primary_key=True)
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    account_type = models.CharField(max_length=50)

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
    objects = BaseUserManager()

    def __str__(self):
        return self.email

    #defines table
    class Meta:
        db_table = 'user'


class CreatedUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True)
    #is_active = models.BooleanField(default=True)
    #is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    #is_anonymous = models.BooleanField(default=False)
    #is_authenticated = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'created_users'


class Cart(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    user_id = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'storestock'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)'''

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission, PermissionsMixin

class StoreStock(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    #seller = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'account_type': 'seller'})


    class Meta:
        db_table = 'StoreStock'

    def __str__(self):
        return f"{self.name} by "#{self.seller.username}"

class User(AbstractUser):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]

    objects = BaseUserManager()
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
        db_table = 'user'

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
        return f"Order {self.order.id} Order Details "

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

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(StoreStock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def item_total(self):
        """Calculate the total price for this cart item."""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"

    class Meta:
        unique_together = ['cart', 'product']