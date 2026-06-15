from django.urls import path

from userauths import views
from userauths import api


app_name = 'userauths'


urlpatterns = [
    path('sign-up/', views.RegisterView.as_view(), name='sign-up'),
    path('sign-in/', views.LoginView.as_view(), name='sign-in'),
    path('user/sign-out/', views.LogoutView.as_view(), name='sign-out'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('phone/edit/<int:pk>/', views.PhoneUpdateView.as_view(), name='phone-edit'),
    path('phone/checkout/edit/<int:pk>/', views.PhoneUpdateCheckoutView.as_view(), name='phone_edit_checkout'),
    path('phone/create/', views.PhoneCreateView.as_view(), name='phone_create'),
    path('phone/delete/<int:pk>/', views.delete_phone, name='phone_delete'),
    path('phone/delete/checkout/<int:pk>/', views.delete_phone_checkout, name='phone_delete_checkout'),
    path('phone/create/checkout/', views.PhoneCreateCheckoutView.as_view(), name='phone_create_checkout'),
    path('address/edit/<int:pk>/', views.AddressUpdateView.as_view(), name='address_edit'),
    path('address/edit/checkout/<int:pk>/', views.AddressUpdateCheckoutView.as_view(), name='address_edit_checkout'),
    path('address/delete/<int:pk>/', views.delete_address, name='address_delete'),
    path('address/delete/checkout/<int:pk>/', views.delete_address_checkout, name='address_delete_checkout'),
    path('address/add/', views.add_address, name='add_address'),
    path('add/address/checkout', views.add_address_checkout, name='add_address_checkout'),
    path('add-card/', views.add_credit_card, name='add_card'),
    path('add-card/checkout', views.add_credit_card_checkout, name='add_card_checkout'),
    path('delete-card/<int:pk>/', views.delete_credit_card, name='delete_card'),
    path('delete-card/checkout/<int:pk>/', views.delete_credit_card_checkout, name='delete_card_checkout'),
    path("reset-password/", views.send_reset_email, name="send_reset_email"),
    path("reset-password/<uuid:token>/", views.reset_password, name="reset_password"),

    # api 
    path('api/<int:pk>/', api.UserRetrieveUpdateDestroyAPIView.as_view(), name='user_api_updc'),
    path('api/', api.UserListAPIView.as_view(), name='user_api_list'),
    path('api/create/', api.UserCreateAPIView.as_view(), name='user_api_create'),
    path('api/profile/', api.ProfileListAPIView.as_view(), name='profile_api_list'),
    path('api/profile/create/', api.ProfileCreateAPIView.as_view(), name='profile_api_create'),
    path('api/profile/update/<pk>/', api.ProfileUpdateAPIView.as_view(), name='profile_api_update'),
]