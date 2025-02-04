from rest_framework import serializers
from .models import Product

# Serializator dla modelu Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image']
