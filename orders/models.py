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
        
