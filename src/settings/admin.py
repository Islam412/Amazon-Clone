from django.contrib import admin
from .models import Company , DeliveryFee , FreeOffer

# Register your models here.

admin.site.register(Company)
admin.site.register(DeliveryFee)
admin.site.register(FreeOffer)
