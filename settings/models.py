from django.db import models
from django.utils.timezone import now


# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logos')
    subtitle = models.TextField(max_length=1000, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    instgram_link = models.URLField(max_length=200, null=True, blank=True)
    twitter_link = models.URLField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phones = models.CharField(max_length=255, null=True, blank=True)
    android_app = models.URLField(max_length=200, null=True, blank=True)
    ios_app = models.URLField(max_length=200, null=True, blank=True)
    call_us = models.CharField(max_length=255, null=True, blank=True)
    email_us = models.CharField(max_length=255, null=True, blank=True)
    free_home_delivery = models.CharField(max_length=255, null=True, blank=True)
    instant_return_policy = models.CharField(max_length=255, null=True, blank=True) 
    support_system = models.CharField(max_length=255, null=True, blank=True)
    secure_payment_way = models.CharField(max_length=255, null=True, blank=True)
    android_ios_app = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name



class DeliveryFee(models.Model):
    fee = models.FloatField(null=True, blank=True)
    def __str__(self):
        return str(self.fee)



class FreeOffer(models.Model):
    title = models.CharField(max_length=225 , null=True , blank=True)
    description = models.TextField(max_length=1000 , null=True , blank=True)
    image = models.ImageField(upload_to='product_fee')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


