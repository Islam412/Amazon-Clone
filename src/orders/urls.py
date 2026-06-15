from django.urls import path

from .views import OrderListView, checkout , add_to_cart , remove_from_cart , remove_from_checkout , process_payment , payment_success , payment_failed , coupon , wishlist_view , remove_from_wishlist , add_to_wishlist
from .api import CartDetailCreateAPI , OrderListAPI , OrderDetailsAPI , CreateOrderAPI , ApplyCouponAPI



app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('checkout/', checkout, name='checkout'),
    path('coupon/', coupon, name='coupon'),
    path('checkout/payment/', process_payment, name='process_payment'),
    path('checkout/payment/success', payment_success),
    path('checkout/payment/failed', payment_failed),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>', remove_from_cart, name='remove_from_cart'),
    path('remove-from-checkout/<int:id>', remove_from_checkout, name='remove_from_checkout'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:pk>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),

    # api
    path('api/list/<str:username>' ,OrderListAPI.as_view(), name='OrderListAPI'),
    path('api/list/<str:username>/create-order' ,CreateOrderAPI.as_view(), name='CreateOrderAPI'),
    path('api/list/<str:username>/<int:pk>' ,OrderDetailsAPI.as_view(), name='OrderDetailsAPI'),
    path('api/<str:username>/cart' ,CartDetailCreateAPI.as_view(), name='CartDetailCreateAPI'),
    path('api/<str:username>/cart/apply-coupon' ,ApplyCouponAPI.as_view(), name='CartDetailCreateAPI'),
]
