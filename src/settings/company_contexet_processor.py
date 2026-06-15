from .models import Company , DeliveryFee , FreeOffer


def get_company_data(request):
    data = Company.objects.last()
    # fee = DeliveryFee.objects.last()
    return {'company_data': data }


def get_offer_data(request):
    data = FreeOffer.objects.last()
    return {'offer_data': data }