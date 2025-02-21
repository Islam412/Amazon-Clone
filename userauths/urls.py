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
    path('phone/create/', views.PhoneCreateView.as_view(), name='phone_create'),
    path('phone/delete/<int:pk>/', views.delete_phone, name='phone_delete'),

    # api 
    path('api/<int:pk>/', api.UserRetrieveUpdateDestroyAPIView.as_view(), name='user_api_updc'),
    path('api/', api.UserListAPIView.as_view(), name='user_api_list'),
    path('api/create/', api.UserCreateAPIView.as_view(), name='user_api_create'),
    path('api/profile/', api.ProfileListAPIView.as_view(), name='profile_api_list'),
    path('api/profile/create/', api.ProfileCreateAPIView.as_view(), name='profile_api_create'),
    path('api/profile/update/<pk>/', api.ProfileUpdateAPIView.as_view(), name='profile_api_update'),
]