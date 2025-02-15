from django.shortcuts import render , redirect
from django.views.generic import ListView , DetailView
from django.db.models import Q , F , Value , Count
from django.db.models.aggregates import Max,Min,Count,Avg,Sum
from django.views.decorators.cache import cache_page # python raises py caching exceptions
from django.http import JsonResponse
from django.template.loader import render_to_string



from .models import Product, Brand, ProductImage, Review
from .tasks import send_email


@cache_page(60 * 1)
def queryset_debug(request):
    
    # data = Product.objects.all()
    
    # data = Product.objects.filter(price__gt=80, quantity__lt=10)  #and
    
    # data = Product.objects.filter(Q(price__gt=80) & Q(quantity__lt=10))  #or
    
    # data = Product.objects.annotate(price_with_tax=F('price')*1.2) # add new tower

    data = Product.objects.all()

    
    return render(request, 'products/queryset_debug.html', {'data': data})