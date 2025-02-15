from rest_framework import serializers

from .models import Cart , CartDetails , Order , OrderDetails
from products.serializers import ProductListSerializers , ProductCartSerializers


class CartDetailSerializer(serializers.Serializer):
    product = ProductCartSerializers()
    # product = serializers.StringRelatedField()
    class Meta:
        model = CartDetails
        fields = '__all__'