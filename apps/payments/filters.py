from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.djalalidates.filters import filter_date
from apps.basicusers.models import MidUser
from apps.orders.models import Order
from apps.receptionists.models import Receptionist

class PaymentFilter(FilterSet):
    user=ModelChoiceFilter(field_name='user__public_id',queryset=MidUser.objects.all())
    order=ModelChoiceFilter(field_name='order__public_id',queryset=Order.objects.all())

    created_date = CharFilter(method=filter_date)
    created_date__lte = CharFilter( method=filter_date)
    created_date__gte= CharFilter( method=filter_date)
   
    class Meta:
        model=Payment
        fields={
            'amount':['range','exact'],
            'status':['exact'],
            'created_time':['range','lte','gte','exact']
        }

class ReceptionistPaymentFilter(FilterSet):
    user=ModelChoiceFilter(field_name='user__public_id',queryset=Receptionist.objects.all())

    created_date = CharFilter(method=filter_date)
    created_date__lte = CharFilter( method=filter_date)
    created_date__gte= CharFilter( method=filter_date)
    updated_date = CharFilter(method=filter_date)
    updated_date__lte = CharFilter( method=filter_date)
    updated_date__gte= CharFilter( method=filter_date)
   
    class Meta:
        model=RecpetionistPayment
        fields={
            'salary':['exact','range','lte','gte'],
            'created_time':['range','lte','gte','exact'],
            'updated_time':['range','lte','gte','exact']
        }

class WithdrawalRequestFilter(FilterSet):
    user=ModelChoiceFilter(field_name='user__public_id',queryset=MidUser.objects.all())

    created_date = CharFilter(method=filter_date)
    created_date__lte = CharFilter( method=filter_date)
    created_date__gte= CharFilter( method=filter_date)
    paid_date = CharFilter(method=filter_date)
    paid_date__lte = CharFilter( method=filter_date)
    paid_date__gte= CharFilter( method=filter_date)
   
    class Meta:
        model=WithdrawalRequest
        fields={
            'amount':['exact','range','lte','gte'],
            'created_time':['range','lte','gte','exact'],
            'paid_time':['range','lte','gte','exact'],
            'status':['exact']
        }

