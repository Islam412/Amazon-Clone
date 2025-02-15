from .models import Company , DeliveryFee


def get_company_data(request):
    data = Company.objects.last()
    fee = DeliveryFee.objects.last()
    return {'company_data': data , 'fee': fee}