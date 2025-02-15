from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save  # create profile before creat user
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from utils.generate_code import generate_code

# Create your models here.

class User(AbstractUser):
    first_name = models.CharField(_('Frist Name'),max_length=255, null=True, blank=True)
    last_name = models.CharField(_('Last Name'),max_length=255, null=True, blank=True)
    username = models.CharField(_('Username'),max_length=255, unique=True, null=True, blank=True)
    email = models.EmailField(_('Email'),unique=True)

    # Change defult django in adminbanal
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover_images = models.ImageField(_('Cover Image'), upload_to='Images_Profile', null=True, blank=True, default='user.png')
    address = models.OneToOneField('Address', null=True, blank=True, on_delete=models.SET_NULL)
    phone = models.OneToOneField('Phone', null=True, blank=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=10, default=generate_code)
    verified = models.BooleanField(_('Verified'), default=False)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}" if self.user.first_name and self.user.last_name else self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def username(self):
        return self.user.username

    @property
    def address_info(self):
        return self.address.address if self.address else "No address provided"

    @property
    def phone_info(self):
        return self.phone.phone if self.phone else "No phone number provided"

    def __str__(self):
        return self.user.username if self.user and self.user.username else 'Unnamed Profile'