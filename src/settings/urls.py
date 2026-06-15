from django.urls import path
from .views import home , contact , need_help

app_name = 'settings'

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('faq/', need_help, name='faq'),
]