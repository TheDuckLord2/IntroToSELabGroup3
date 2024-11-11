from rest_framework import serializers
from .models import Cart, User, OrderDetails, Order, ShippingInformation, CartItem
from django.contrib.auth.models import AbstractUser
from rest_framework.views import APIView


# serialization takes complicated django models and turns them into python
# forms which can be converted in JSON data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # accepts all data fields, quick and easy
        fields = '__all__'

        def create(self, validated_data):
            user = CustomUser(
                id=validated_data['id'],
                username=validated_data['username'],
                email=validated_data['email'],
                account_type=validated_data.get('account_type', 'default')  # Add default if needed
            )
            user.set_password(validated_data['password'])  # Hashes the password
            user.save()
            return user


class ShippingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingInformation
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'name', 'description', 'price', 'stock_quantity']


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields ='__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
