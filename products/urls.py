from django.urls import path
from .views import ProductDetails, ProductList, BrandList, BrandDetails, queryset_debug , product_search , product_filter , product_filter_by_flag , send_emails , add_review 
from .api import product_list_api , product_detail_api , ProductListAPI , ProductDetailAPI , BrandListAPI , BrandDetailAPI

app_name = 'products'

urlpatterns = [
    path('brands/', BrandList.as_view(), name='brand_list'),
    path('search/', product_search, name='product_search'),
    path('filter/', product_filter, name='product_filter'),
    path('<slug:slug>/add-review', add_review, name='add_review'),
    path('filter-by-tags/', product_filter_by_flag, name='product_filter_by_tags'),
    path('', ProductList.as_view(), name='product_list'),
    path('debug/', queryset_debug, name='queryset_debug'),  # Debugging tool for testing queryset performance.
    path('send-email/', send_emails, name='send_emails'),  # celery with radis
    path('<slug:slug>/', ProductDetails.as_view(), name='product_detail'),
    path('brands/<slug:slug>/', BrandDetails.as_view(), name='brand_detail'),

    #api function
    path('api/list', product_list_api, name='product_api_list'),
    path('api/list/<int:product_name>', product_detail_api , name='product_detail_api'),

    #Api genaric views
    path('api/genariclist', ProductListAPI.as_view()),
    path('api/genariclist/<int:pk>', ProductDetailAPI.as_view()),
    path('api/brandlist', BrandListAPI.as_view()),
    path('api/brandlist/<int:pk>', BrandDetailAPI.as_view()),
]