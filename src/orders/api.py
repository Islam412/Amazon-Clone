from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.response import Response

import datetime

from .serializers import CartDetailSerializer , CartSerializer , OrderListSerializer , OrderDetailsSerializer
from .models import Cart , CartDetails , Order, OrderDetails ,Coupon
from products.models import Product
from userauths.models import User



class CartDetailCreateAPI(generics.GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def get(self,request,*args,**kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart,created = Cart.objects.get_or_create(user=user,status='InProgress')
        data = CartSerializer(cart).data
        return Response({'cart':data})
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        product = Product.objects.get(id=request.data['product_id'])
        quantity = int(request.data['quantity'])
        cart = Cart.objects.get(user=user,status='InProgress')
        cart_detail , creeate = CartDetails.objects.get_or_create(cart=cart, product=product)
        cart_detail.quantity = int(quantity)
        cart_detail.total = round(quantity * product.price , 2)
        cart_detail.save()

        cart = Cart.objects.get(user=user,status='InProgress')
        data = CartSerializer(cart).data
        return Response({'message':'Cart item added successfully' ,'cart':data})

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart_detail =CartDetails.objects.get(id=request.data['cart_detail_id'])
        cart_detail.delete()

        cart = Cart.objects.get(user=user,status='InProgress')
        data = CartSerializer(cart).data
        return Response({'message':'Cart product deleted successfully' ,'cart':data})
    



class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [AllowAny]
    queryset = Order.objects.all()

    def list(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        queryset = self.get_queryset().filter(user=user)
        data = OrderListSerializer(queryset, many=True).data
        return Response(data)




class OrderDetailsAPI(generics.RetrieveAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [AllowAny]
    queryset = Order.objects.all()




class CreateOrderAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart = Cart.objects.get(user=user,status='InProgress')
        cart_details = CartDetails.objects.filter(cart=cart)

        # cart create order
        new_order = Order.objects.create(
            user = user,
            coupon = cart.coupon,
            total_after_coupon = cart.total_after_coupon,
        )

        # cart detail --->order detail-->loop
        for object in cart_details:
            OrderDetails.objects.create(
                order = new_order,
                product = object.product,
                quantity = object.quantity,
                price = object.product.price,
                total = round(int(object.quantity)*object.product.price,2),
            )

        cart.status = 'Completed'
        cart.save()
        return Response({'message':'Order created successfully'})




class ApplyCouponAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=self.kwargs['username'])
        cart = Cart.objects.get(user=user,status='InProgress')

        coupon = get_object_or_404(Coupon,code=request.data['coupon_code']) # 404 with out coupon
        # coupon = Coupon.objects.get(code=request.data['coupon_code']) # erorr without coupon

        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()

            if today_date >= coupon.start_date and coupon.end_date:
                coupon_value = cart.cart_total() * coupon.discount/100
                cart_total = cart.cart_total() - coupon_value

                coupon.quantity -= 1
                coupon.save()

                cart.coupon = coupon
                cart.total_after_coupon = cart_total
                cart.save()

                cart = Cart.objects.get(user=user,status='InProgress')
                data = CartSerializer(cart).data
                return Response({'message':'Coupon applying successfully','cart':data})
            else:
                return Response({'message':'Coupon is expired'})
        else:
            return Response({'message':'Coupon is not found'})