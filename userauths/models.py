from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save  # create profile before creat user
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from utils.generate_code import generate_code


import uuid


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


@receiver(post_save, sender=User)
# create user profile automatic
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile ,sender=User)
post_save.connect(save_user_profile ,sender=User)



ADDRESS_TYPE = [
    ('Home', 'Home'),
    ('Business','Business'),
    ('Office','Office'),
    ('Academy','Academy'),
    ('Other','Other'),
]

class Address(models.Model):
    user = models.ForeignKey(User,related_name='user_address',on_delete=models.CASCADE)
    type = models.CharField(_('Type'),max_length=20,choices=ADDRESS_TYPE)
    address = models.TextField(_('address'),max_length=300)
    notes = models.TextField(_('Notes'),null=True,blank=True)

    def __str__(self):
        return f"{self.type} - {self.address}"


Phone_TYPE = [
    ('Primary','Primary'),
    ('Secondary','Secondary'),
    ('Third','Third')
]


class Phone(models.Model):
    user = models.ForeignKey(User, related_name='user_phone', on_delete=models.CASCADE)
    type = models.CharField(_('type'),max_length=20, choices=Phone_TYPE)
    phone = models.CharField(_('phone'),max_length=30)

    def clean(self):
        if not self.phone.isdigit():
            raise ValidationError("Phone number must be numeric.")

    def __str__(self):
        return f"{self.type} - {self.phone}"


@receiver(post_save, sender=Address)
def create_or_update_profile_with_address(sender, instance, created, **kwargs):
    if instance.user.profile:
        instance.user.profile.address = instance
        instance.user.profile.save()

@receiver(post_save, sender=Phone)
def create_or_update_profile_with_phone(sender, instance, created, **kwargs):
    if instance.user.profile:
        instance.user.profile.phone = instance
        instance.user.profile.save()


class CreditCard(models.Model):
    user = models.ForeignKey(User, related_name='user_credit_cards', on_delete=models.CASCADE)
    image = models.ImageField(_('Image'), upload_to='Images_credit', null=True, blank=True, default='credit.webp')
    name = models.CharField(_('Name'),max_length=225)
    card_number = models.CharField(_('Card Number'),max_length=16)
    country = models.CharField(_('Country'),max_length=225)
    cvv = models.CharField(_('CVV'),max_length=3)
    expiration_date = models.DateField(_('Expiration Date'),)

    def __str__(self):
        return f"Card ending in {self.card_number[-4:]} - {self.user.username}"





User = get_user_model()

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(default=now)

    def is_valid(self):
        return (now() - self.created_at).total_seconds() < 1800 

    def __str__(self):
        return f"Reset token for {self.user.email}"
