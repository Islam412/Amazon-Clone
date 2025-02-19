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

    def total_items(self):
        return sum(detail.quantity for detail in self.order_details.all())



class OrderDetails(models.Model):
    order = models.ForeignKey(Order,related_name='order_details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.FloatField(('Price'))
    quantity = models.IntegerField(_('Quantity'))
    total = models.FloatField(_('Total'), null=True,blank=True)

    def __str__(self):
        return str(self.order)

    def save(self, *args, **kwargs):
        if self.product and not self.price:
            self.price = self.product.price 

        self.total = self.price * self.quantity
        super().save(*args, **kwargs)




class Coupon(models.Model):
    image = models.ImageField(_('Image'),upload_to='coupon', blank=True, null=True)
    code = models.CharField(_('Code'), max_length=20)
    discount = models.IntegerField(_('Discount'))
    quantity = models.IntegerField(_('Quantity'))
    start_date = models.DateField(_('Start Date'), default=timezone.now)
    end_date = models.DateField(_('End Date'), null=True,blank=True)

    def __str__(self):
        return self.code
    

    def save(self, *args, **kwargs):
       week = datetime.timedelta(days=7)
       self.end_date = self.start_date + week
       super(Coupon, self).save(*args, **kwargs)  # call the real save method



class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name='wishlist_user', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='wishlist_product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product}"
