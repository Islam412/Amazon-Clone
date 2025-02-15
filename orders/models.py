from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from userauths.models import User
from products.models import Product

import datetime
import random

# Create your models here.

CART_STATUS = [
    ('InProgress','InProgress'),
    ('Completed','Completed'),
]

class Cart(models.Model):
    user = models.ForeignKey(User,related_name='cart_user', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(_('Status'),max_length=10,choices=CART_STATUS)
    coupon = models.ForeignKey('Coupon',related_name='cart_coupon', on_delete=models.SET_NULL, blank=True , null=True)
    total_after_coupon = models.FloatField(_('Total After Coupon'),null=True,blank=True)


    def __str__(self):
        return str(self.user)
    
    def cart_total(self):
        total = 0
        for item in self.cart_details.all():
            total += item.total
        return round(total,2)

    def discount_amount(self):
        if self.total_after_coupon:
            return round(self.cart_total() - self.total_after_coupon, 2)
        return 0.0



class CartDetails(models.Model):
    cart = models.ForeignKey(Cart,related_name='cart_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_product', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(_('Quantity'),default=1)
    total = models.FloatField(_('Total'),null=True,blank=True)

    def __str__(self):
        return str(self.cart)



def generate_code(length=10):
    data = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = ''.join(random.choice(data) for _ in range(length))
    return code


ORDER_STATUS = [
    ('Recieved','Recieved'),
    ('Processed','Processed'),
    ('Shipped','Shipped'),
    ('Delivered','Delivered'),
]
class Order(models.Model):
    user = models.ForeignKey(User,related_name='order_user', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(('Status'), max_length=10,choices=ORDER_STATUS,default='Recieved')
    code = models.CharField(_('Code'), max_length=20,default=generate_code)
    order_time = models.DateTimeField(default=timezone.now)
    delivery_time = models.DateTimeField(_('Delivery Time'),null=True, blank=True)
    coupon = models.ForeignKey('Coupon',related_name='order_coupon', on_delete=models.SET_NULL, blank=True , null=True)
    total_after_coupon = models.FloatField(_('Total After Coupon'),null=True,blank=True)

    def __str__(self):
        return str(self.user)
    