# from .models import Profile, Phone, Address, ADDRESS_TYPE, CreditCard

# def get_profile_data(request):
#     if not request.user.is_authenticated:
#         return {
#             'profile_data': None,
#             'primary_phone': "No Primary Phone",
#             'secondary_phone': "No Secondary Phone",
#             'third_phone': "No Third Phone",
#             'addresses': [],
#             'address_types': ADDRESS_TYPE,
#             'credit_cards': [],
#         }

#     profile_data = Profile.objects.filter(user=request.user).first()

#     if profile_data:

#         phone_numbers = Phone.objects.filter(user=request.user)

#         primary_phone = phone_numbers.filter(type='Primary').first()
#         secondary_phone = phone_numbers.filter(type='Secondary').first()
#         third_phone = phone_numbers.filter(type='Third').first()

#         addresses = Address.objects.filter(user=request.user)

#         credit_cards = CreditCard.objects.filter(user=request.user)

#         context = {
#             'profile_data': profile_data,
#             'primary_phone': primary_phone.phone if primary_phone else "No Primary Phone",
#             'secondary_phone': secondary_phone.phone if secondary_phone else "No Secondary Phone",
#             'third_phone': third_phone.phone if third_phone else "No Third Phone",
#             'addresses': addresses,
#             'address_types': ADDRESS_TYPE,
#             'credit_cards': credit_cards,
#         }
#     else:
#         context = {
#             'profile_data': None,
#             'primary_phone': "No Primary Phone",
#             'secondary_phone': "No Secondary Phone",
#             'third_phone': "No Third Phone",
#             'addresses': [],
#             'address_types': ADDRESS_TYPE,
#             'credit_cards': [],
#         }

#     return context



from .models import Profile, Phone, Address, ADDRESS_TYPE, CreditCard

def get_profile_data(request):
    if not request.user.is_authenticated:
        return {
            'profile_data': None,
            'primary_phone': None,
            'secondary_phone': None,
            'third_phone': None,
            'addresses': [],
            'address_types': ADDRESS_TYPE,
            'credit_cards': [],
        }

    profile_data = Profile.objects.filter(user=request.user).first()

    if profile_data:
        phone_numbers = Phone.objects.filter(user=request.user)

        primary_phone = phone_numbers.filter(type='Primary').first()
        secondary_phone = phone_numbers.filter(type='Secondary').first()
        third_phone = phone_numbers.filter(type='Third').first()

        addresses = Address.objects.filter(user=request.user)
        credit_cards = CreditCard.objects.filter(user=request.user)

        context = {
            'profile_data': profile_data,
            'primary_phone': primary_phone,
            'secondary_phone': secondary_phone,
            'third_phone': third_phone,
            'addresses': addresses,
            'address_types': ADDRESS_TYPE,
            'credit_cards': credit_cards,
        }
    else:
        context = {
            'profile_data': None,
            'primary_phone': None,
            'secondary_phone': None,
            'third_phone': None,
            'addresses': [],
            'address_types': ADDRESS_TYPE,
            'credit_cards': [],
        }

    return context
