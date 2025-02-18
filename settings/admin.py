from django.contrib import admin
from .models import Company , DeliveryFee , FeeOffer

# Register your models here.

admin.site.register(Company)
admin.site.register(DeliveryFee)
admin.site.register(FeeOffer)
