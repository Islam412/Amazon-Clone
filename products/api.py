from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters

from .serializers import ProductListSerializers , ProductDetailSerializers , BrandListSerializers , BrandDetailSerializers
from .models import Product , Brand
from .myfilter import ProductFilter


# Functions api
@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()[:20]
    data = ProductListSerializers(products, many=True , context={'request':request}).data
    return Response({'products':data})



@api_view(['GET','POST'])  # GET Show all data | POST Update data
def product_detail_api(request,product_name):
    products = Product.objects.get(id=product_name)
    data = ProductDetailSerializers(products, context={'request':request}).data
    return Response({'products':data})



# class generic view api

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
