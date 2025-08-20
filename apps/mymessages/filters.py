from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.djalalidates.filters import filter_date
from apps.basicusers.models import BaseUser

class MessageFilter(FilterSet):
    sender=ModelChoiceFilter(field_name='sender__public_id',queryset=BaseUser.objects.all())
    reciver=ModelChoiceFilter(field_name='reciver__public_id',queryset=BaseUser.objects.all())
    created_date = CharFilter(method=filter_date)
    created_date__gte = CharFilter( method=filter_date)
    created_date__lte = CharFilter( method=filter_date)
    updated_date = CharFilter( method=filter_date)
    updated_date__gte = CharFilter(method=filter_date)
    updated_date__lte = CharFilter( method=filter_date)
    text = CharFilter(field_name='text', lookup_expr='icontains')
    class Meta:
        model=Mymessage
        fields={
            'titel':['iexact'],
            'created_time':['lte','gte','exact'],
            'updated_time':['lte','gte','exact'],
            'read_status':['exact']
        }