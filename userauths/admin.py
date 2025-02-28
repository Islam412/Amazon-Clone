from django.contrib import admin
from userauths.models import User, Profile , Address , Phone , CreditCard , PasswordResetToken

class UserCustomAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['email']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ('user_permissions',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'username', 'address_info', 'phone_info', 'verified']  # إضافة 'full_name', 'email', 'username'
    list_editable = ['verified']
    search_fields = ['user__username', 'phone', 'address']
    list_filter = ['verified']
    ordering = ['user']

admin.site.register(User, UserCustomAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(CreditCard)
admin.site.register(PasswordResetToken)
