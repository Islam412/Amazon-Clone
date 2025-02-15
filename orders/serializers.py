from rest_framework import serializers

from .models import Cart , CartDetails , Order , OrderDetails
from products.serializers import ProductListSerializers , ProductCartSerializers


class CartDetailSerializer(serializers.Serializer):
    product = ProductCartSerializers()
    # product = serializers.StringRelatedField()
    class Meta:
        model = CartDetails
        fields = '__all__'



class CartSerializer(serializers.ModelSerializer):
    cart_details = CartDetailSerializer(many=True)
    coupon = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = '__all__'



class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = '__all__'



class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = OrderProductSerializer(many=True, source='order_details')

    class Meta:
        model = Order
        fields = '__all__'