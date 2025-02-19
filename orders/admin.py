from django.contrib import admin
from .models import Cart,CartDetails,Order,OrderDetails,Coupon,Wishlist

# Register your models here.



admin.site.register(Cart)
admin.site.register(CartDetails)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Coupon)
admin.site.register(Wishlist)
