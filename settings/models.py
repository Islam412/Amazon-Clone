from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Company(models.Model):
    name = models.CharField(_('name'),max_length=255)
    logo = models.ImageField(_('logo'),upload_to='company_logos')
    subtitle = models.TextField(_('subtitle'),max_length=1000, null=True, blank=True)
    facebook_link = models.URLField(_('facebook'),max_length=200, null=True, blank=True)
    instgram_link = models.URLField(_('instgram'),max_length=200, null=True, blank=True)
    twitter_link = models.URLField(_('twitter'),max_length=200, null=True, blank=True)
    email = models.EmailField(_('email'),max_length=200, null=True, blank=True)
    address = models.CharField(_('address'),max_length=255, null=True, blank=True)
    phones = models.CharField(_('phones'),max_length=255, null=True, blank=True)
    android_app = models.URLField(_('android app'),max_length=200, null=True, blank=True)
    ios_app = models.URLField(_('ios app'),max_length=200, null=True, blank=True)
    call_us = models.CharField(_('call us'),max_length=255, null=True, blank=True)
    email_us = models.CharField(_('email us'),max_length=255, null=True, blank=True)
    free_home_delivery = models.CharField(_('free home delivery'),max_length=255, null=True, blank=True)
    instant_return_policy = models.CharField(_('instant return policy'),max_length=255, null=True, blank=True) 
    support_system = models.CharField(_('support system'),max_length=255, null=True, blank=True)
    secure_payment_way = models.CharField(_('secure payment way'),max_length=255, null=True, blank=True)
    android_ios_app = models.CharField(_('android ios app'),max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name



class DeliveryFee(models.Model):
    fee = models.FloatField(_('fee'))
    def __str__(self):
        return str(self.fee)



class FreeOffer(models.Model):
    title = models.CharField(_('title'),max_length=225 , null=True , blank=True)
    description = models.TextField(_('description'),max_length=1000 , null=True , blank=True)
    image = models.ImageField(_('image'),upload_to='product_fee')
    created_at = models.DateTimeField(_('created_at'),default=now)

    def __str__(self):
        return self.title


