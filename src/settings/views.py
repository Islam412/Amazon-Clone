from django.shortcuts import render
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.timezone import now, timedelta


from products.models import Product , Brand , Review 
from .models import FreeOffer

# Create your views here.
# from django.contrib.auth.decorators import login_required
# @login_required
# @cache_page(60 * 60 * 24)
def home(request):
    brands = Brand.objects.all().annotate(products_count=Count('product_name'))
    sale_products = Product.objects.filter(flag='Sale')[:15]
    featured_products = Product.objects.filter(flag='Feature')[:6]
    new_products = Product.objects.filter(flag='New')[:15]
    review = Review.objects.all()[:6]
    
    return render(request, 'settings/home.html', {
        'brands': brands,
        'sale_products': sale_products,
        'featured_products': featured_products,
        'new_products': new_products,
        'review': review
    }) 


def contact(request):
    return render(request, 'settings/contact.html')


def need_help(request):
    return render(request, 'settings/need_help.html')

