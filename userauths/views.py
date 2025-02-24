from django.views.generic.edit import FormView ,UpdateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect ,get_object_or_404 ,render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse
from django.views.decorators.http import require_POST



from userauths.models import User , Profile , Address , Phone
from userauths.forms import UserRegisterForm , ProfileForm , CustomPasswordChangeForm , PhoneUpdateForm , AddressUpdateForm
from userauths.serializers import UserSerializer , ProfileSerializer 




class RegisterView(FormView):
    template_name = 'userauths/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('settings:home')

    def form_valid(self, form):
        user = form.save()
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Hi {user.username}, your account has been created successfully.")
            return super().form_valid(form)
        return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error with your registration.")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, f"Hey {request.user.username}, you are already logged in")
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)



class LoginView(TemplateView):
    template_name = 'userauths/login.html'

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                return redirect('settings:home')
            else:
                messages.error(request, 'Username or password does not exist.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        return redirect('userauths:login')  # Redirect back to login on failure

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('settings:home')
        return super().get(request, *args, **kwargs)



class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'userauths/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect("userauths:sign-in")
    



# @login_required
class ProfileView(DetailView):
    model = Profile
    template_name = 'userauths/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
    

    # return data off phoens and adsress and credit cards
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['phones'] = self.get_object().user.user_phone.all()
        context['address'] = self.get_object().user.user_address.all()
        context['credit'] = self.get_object().user.user_credit_cards.all() # user_credit_cards ----->the name off lien at db
        return context



# @login_required
class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'userauths/profile_update.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('userauths:profile')




class ChangePasswordView(PasswordChangeView):
    template_name = 'userauths/change-password.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('userauths:profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password was successfully updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error updating your password. Please try again.")
        return super().form_invalid(form)



# for one numper
# class PhoneUpdateView(LoginRequiredMixin, UpdateView):
#     model = Phone
#     form_class = PhoneUpdateForm
#     template_name = 'userauths/phone_update.html'
#     context_object_name = 'phone'

#     def get_object(self, queryset=None):
#         return get_object_or_404(Phone, user=self.request.user)

#     def form_valid(self, form):
#         messages.success(self.request, "Your phone number has been updated successfully.")
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy('userauths:profile')


class PhoneUpdateView(LoginRequiredMixin, UpdateView):
    model = Phone
    form_class = PhoneUpdateForm
    template_name = 'userauths/phone_update.html'
    context_object_name = 'phone'

    def get_object(self, queryset=None):
        phone_id = self.kwargs.get('pk')
        return get_object_or_404(Phone, id=phone_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your phone number has been updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('userauths:profile')


class PhoneCreateView(LoginRequiredMixin, FormView):
    form_class = PhoneUpdateForm
    template_name = 'userauths/phone_create.html'
    success_url = reverse_lazy('userauths:profile')

    def form_valid(self, form):
        phone = form.save(commit=False)
        phone.user = self.request.user
        phone.save()
        messages.success(self.request, "Your phone number has been added successfully.")
        return super().form_valid(form)



def delete_phone(request, pk):

    if request.user.is_authenticated and request.method == "POST":
        phone = get_object_or_404(Phone, pk=pk, user=request.user)
        phone.delete()
        return redirect('userauths:profile')

    return redirect('userauths:sign-in')



class PhoneUpdateCheckoutView(LoginRequiredMixin, UpdateView):
    model = Phone
    form_class = PhoneUpdateForm
    template_name = 'userauths/phone_update.html'
    context_object_name = 'phone'

    def get_object(self, queryset=None):
        phone_id = self.kwargs.get('pk')
        return get_object_or_404(Phone, id=phone_id, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Your phone number has been updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('orders:checkout')



def delete_phone_checkout(request, pk):

    if request.user.is_authenticated and request.method == "POST":
        phone = get_object_or_404(Phone, pk=pk, user=request.user)
        phone.delete()
        return redirect('orders:checkout')

    return redirect('userauths:sign-in')



class PhoneCreateCheckoutView(LoginRequiredMixin, FormView):
    form_class = PhoneUpdateForm
    template_name = 'userauths/phone_create.html'
    success_url = reverse_lazy('orders:checkout')

    def form_valid(self, form):
        phone = form.save(commit=False)
        phone.user = self.request.user
        phone.save()
        messages.success(self.request, "Your phone number has been added successfully.")
        return super().form_valid(form)





class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressUpdateForm
    template_name = 'userauths/address_update.html'
    context_object_name = 'address'

    def get_object(self, queryset=None):
        address_id = self.kwargs.get('pk')
        return get_object_or_404(Address, id=address_id, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('userauths:profile')



class AddressUpdateCheckoutView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressUpdateForm
    template_name = 'userauths/address_update.html'
    context_object_name = 'address'

    def get_object(self, queryset=None):
        address_id = self.kwargs.get('pk')
        return get_object_or_404(Address, id=address_id, user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('orders:checkout')



@login_required
@require_POST
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('userauths:profile')



@login_required
@require_POST
def delete_address_checkout(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    return redirect('orders:checkout')




@login_required
def add_address(request):
    if request.method == "POST":
        form = AddressUpdateForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user  
            address.save()
            return redirect('userauths:profile')
    else:
        form = AddressUpdateForm()

    return render(request, 'userauths/add_address.html', {'form': form})