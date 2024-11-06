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


class Inventory(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'storestock'