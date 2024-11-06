from rest_framework import serializers
from .models import UserCreation, Cart, CreatedUser
from django.contrib.auth.models import AbstractUser
from rest_framework.views import APIView


#serialization takes complicated django models and turns them into python
#forms which can be converted in JSON data
class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreation
        #accepts all data fields, quick and easy
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


class CreatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatedUser
        fields = ('email', 'username', 'password')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'