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



def send_emails(request):
    if request.method == 'GET':
        send_email.delay()  
        return render(request, 'products/send_email.html')

    elif request.method == 'POST':
        progress = cache.get('email_progress', 'No progress yet.')
        sent_emails = cache.get('sent_emails', [])
        return JsonResponse({'status': progress, 'sent_emails': sent_emails})



class ProductList(ListView):
    model = Product
    paginate_by = 30
    ordering = ['-id']



class ProductDetails(DetailView):
    model = Product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["reviews"] = Review.objects.filter(product=product)
        context["average_rating"] = product.average_rating
        context["rate_products"] = Product.objects.filter(brand=product.brand)
        return context
    


class BrandList(ListView):
    model = Brand
    queryset = Brand.objects.annotate(products_count=Count('product_name'))
    paginate_by = 20
    ordering = ['-id']