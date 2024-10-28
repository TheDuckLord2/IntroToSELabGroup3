from rest_framework import serializers
from .models import UserCreation, Inventory


#serialization takes complicated django models and turns them into python
#forms which can be converted in JSON data
class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreation
        #accepts all data fields, quick and easy
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'