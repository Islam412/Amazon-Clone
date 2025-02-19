from django.shortcuts import render , redirect , get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required # login required for functions
from django.contrib.auth.mixins import LoginRequiredMixin # login required for class based views
from django.utils import timezone
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic.detail import DetailView


import datetime
import stripe


from .models import Order , CartDetails , Cart , Coupon , OrderDetails , Wishlist
from products.models import Product
from settings.models import DeliveryFee
from utils.generate_code import generate_code
from userauths.models import Profile

# Create your views here.


class OrderListView(LoginRequiredMixin , ListView):
    model = Order
    ordering = ['-id']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset



def add_to_cart(request):
    quantity = request.POST['quantity']
    product = Product.objects.get(id=request.POST['product_id'])

    cart = Cart.objects.get(user = request.user, status='InProgress')
    cart_detail , creeate = CartDetails.objects.get_or_create(cart=cart, product=product)

    cart_detail.quantity = int(quantity)
    cart_detail.total = round(int(quantity) * product.price , 2)
    cart_detail.save()

    return redirect (f'/products/{product.slug}')


def remove_from_cart(request,id):
    cart_detail = CartDetails.objects.get(id=id)
    cart_detail.delete()
    return redirect('/products/')



def remove_from_checkout(request,id):
    cart_detail = CartDetails.objects.get(id=id)
    cart_detail.delete()
    return redirect('/orders/checkout')



@login_required 
def checkout(request):
    cart = Cart.objects.get(user=request.user,status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE

    if request.method == 'POST':
        coupon = get_object_or_404(Coupon,code=request.POST['coupon_code']) # 404 with out coupon
        # coupon = Coupon.objects.get(code=request.data['coupon_code']) # erorr without coupon


        if coupon and coupon.quantity > 0:
            today_date = datetime.datetime.today().date()

            if today_date >= coupon.start_date and coupon.end_date:
                coupon_value = cart.cart_total() * coupon.discount/100
                cart_total = cart.cart_total() - coupon_value

                coupon.quantity -= 1
                coupon.save()

                cart.coupon = coupon
                cart.total_after_coupon = cart_total
                cart.save()

                total = delivery_fee + cart_total

                cart = Cart.objects.get(user=request.user,status='InProgress')

                html = render_to_string('include/checkout_table.html',{
                    'cart_detail': cart_detail,
                    'sub_total': cart_total,
                    'cart_total': total,
                    'coupon': coupon_value,
                    'delivery_fee': delivery_fee,
                    'pub_key':pub_key,
                })
                return JsonResponse({'result': html})

                # return render(request, 'orders/checkout.html',{
                #     'cart_detail': cart_detail,
                #     'sub_total': cart_total,
                #     'cart_total': total,
                #     'coupon': coupon_value,
                #     'delivery_fee': delivery_fee,
                # })
    else:
        sub_total = cart.cart_total()
        total = delivery_fee + cart.cart_total()
        coupon = 0

    return render(request, 'orders/checkout.html',{
        'cart_detail': cart_detail,
        'sub_total': sub_total,
        'cart_total': total,
        'coupon': coupon,
        'delivery_fee': delivery_fee,
        'pub_key':pub_key,
    })




def process_payment(request):
    cart = Cart.objects.get(user=request.user, status='InProgress')

    if not cart:
        return JsonResponse({'error': 'No active cart found'}, status=400)

    cart_detail = CartDetails.objects.filter(cart=cart)
    delivery_fee = DeliveryFee.objects.last().fee

    if cart.total_after_coupon:
        total = cart.total_after_coupon + delivery_fee
    else:
        total = cart.cart_total() + delivery_fee

    code = generate_code()

    stripe.api_key = settings.STRIPE_API_KEY_SECRET


    items = [
        {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': code,
                },
                'unit_amount': int(total * 100),
            },
            'quantity': 1,
        }
    ]

    checkout_session = stripe.checkout.Session.create(
        line_items=items,
        mode='payment',
        success_url="http://127.0.0.1:8000/orders/checkout/payment/success",  # استخدام HTTPS هنا
        cancel_url="http://127.0.0.1:8000/orders/checkout/payment/failed",  # استخدام HTTPS هنا
    )

    return JsonResponse({'session': checkout_session})



def payment_success(request):

    cart = Cart.objects.get(user=request.user, status='InProgress')
    cart_detail = CartDetails.objects.filter(cart=cart)

    new_order = Order.objects.create(
        user=request.user,
        coupon=cart.coupon,
        total_after_coupon=cart.total_after_coupon,
    )

    for item in cart_detail:
        OrderDetails.objects.create(
            order=new_order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
            total=round(item.quantity * item.product.price, 2),
        )

    cart.status = 'Completed'
    cart.save()

    return render(request, 'orders/success.html')



def payment_failed(request):
    return render(request,'orders/failed.html')


def coupon(request):
    coupon = Coupon.objects.all()
    context={
        'coupon': coupon,
    }
    return render(request,'orders/coupon.html',context)



def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        context = {
            'wishlist_items': wishlist_items,
        }
        return render(request, 'orders/wishlist.html', context)
    else:
        return redirect('userauths:sign-in')



def remove_from_wishlist(request, pk):
    if request.user.is_authenticated:
        wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)
        wishlist_item.delete()
        return redirect('orders:wishlist')
    return redirect('userauths:sign-in')



@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wishlist_item.delete()
    
    return redirect('orders:wishlist')
