from .models import Profile, Phone, Address, ADDRESS_TYPE, CreditCard

def get_profile_data(request):
    profile_data = Profile.objects.filter(user=request.user).first()
    if profile_data:
        # Retrieve all phone numbers associated with the user
        phone_numbers = Phone.objects.filter(user=request.user)
        
        # Categorize phone numbers by type
        primary_phone = phone_numbers.filter(type='Primary').first()
        secondary_phone = phone_numbers.filter(type='Secondary').first()
        third_phone = phone_numbers.filter(type='Third').first()

        # Retrieve all addresses associated with the user
        addresses = Address.objects.filter(user=request.user)

        # Retrieve all credit cards associated with the user
        credit_cards = CreditCard.objects.filter(user=request.user)

        context = {
            'profile_data': profile_data,
            'primary_phone': primary_phone.phone if primary_phone else "No Primary Phone",
            'secondary_phone': secondary_phone.phone if secondary_phone else "No Secondary Phone",
            'third_phone': third_phone.phone if third_phone else "No Third Phone",
            'addresses': addresses,  # Include all user addresses
            'address_types': ADDRESS_TYPE,  # Include all address types as tuples
            'credit_cards': credit_cards,  # Include all credit cards
        }
    else:
        context = {
            'profile_data': None,
            'primary_phone': "No Primary Phone",
            'secondary_phone': "No Secondary Phone",
            'third_phone': "No Third Phone",
            'addresses': [],
            'address_types': ADDRESS_TYPE,  # Return address types even if no profile data exists
            'credit_cards': [],  # Empty list if no profile data exists
        }

    return context
