
from .models import Cart, CartDetails , Wishlist
from settings.models import DeliveryFee


def get_wishlist_items(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return {
            'wishlist_items': wishlist_items,
        }
    return {}


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, status='InProgress')
        cart_detail = CartDetails.objects.filter(cart=cart)
        
        sub_total = round(cart.cart_total(), 2)

        coupon_value = 0
        if cart.total_after_coupon:
            coupon_value = round(sub_total - cart.total_after_coupon, 2)

        delivery_fee = DeliveryFee.objects.last().fee if DeliveryFee.objects.last() else 0
        cart_total = round((cart.total_after_coupon if cart.total_after_coupon else sub_total) + delivery_fee, 2)

        return {
            'cart_data': cart,
            'cart_detail_data': cart_detail,
            'sub_total': sub_total,
            'coupon': coupon_value,
            'delivery_fee': round(delivery_fee, 2),
            'cart_total': cart_total,
        }

    return {}




# from .models import Cart, CartDetails

# def get_or_create_cart(request):
#     if request.user.is_authenticated:
#         cart, created = Cart.objects.get_or_create(user=request.user, status='InProgress')
#         if not created:
#             cart_detail = CartDetails.objects.filter(cart=cart)  # Renamed cart_detail to cart_detail_data
#             return {'cart_data': cart, 'cart_detail_data': cart_detail}  # Renamed cart_detail to cart_detail_data
#         return {'cart_data': cart}
#     else:
#         return {}

