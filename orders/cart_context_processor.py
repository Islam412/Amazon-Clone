from .models import Cart, CartDetails

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, status='InProgress')
        if not created:
            cart_detail = CartDetails.objects.filter(cart=cart)  # Renamed cart_detail to cart_detail_data
            return {'cart_data': cart, 'cart_detail_data': cart_detail}  # Renamed cart_detail to cart_detail_data
        return {'cart_data': cart}
    else:
        return {}