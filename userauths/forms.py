from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

from userauths.models import User , Profile , Address , Phone



class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'First Name'}), max_length=100, required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Last Name'}), max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Username'}), max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;' , 'id': "", 'placeholder':'Email Address'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;', 'id': "", 'placeholder':'Confirm Password'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1' , 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'with-border'




class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;',
            'placeholder': 'Old Password'
        }),
        required=True
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;',
            'placeholder': 'New Password'
        }),
        required=True
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px; border: 2px solid #ccc; background-color: #F5F5F5; border-radius: 6px; height: 40px; padding: 10px;',
            'placeholder': 'Confirm New Password'
        }),
        required=True
    )



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )


    class Meta:
        model = Profile
        fields = ['cover_images']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        self.fields['username'].initial = self.instance.user.username

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            profile.save()

        return profile



class PhoneUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Phone
        fields = ['type' , 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must be numeric.")
        return phone



class AddressUpdateForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
        required=True
    )

    class Meta:
        model = Address
        fields = ['type', 'address', 'notes']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Additional notes', 'rows': 2}),
        }