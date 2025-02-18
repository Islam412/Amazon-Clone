from django.urls import path
from .views import home , contact , need_help , free_offer_list

app_name = 'settings'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('faq/', need_help, name='faq'),
    path('offers/', free_offer_list, name='free_offer_list'),
]