from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.djalalidates.filters import filter_date

class MessageFilter(FilterSet):
    sender=ModelChoiceFilter(field_name='sender__public_id',queryset=MidUser.objects.all())
    reciver=ModelChoiceFilter(field_name='reciver__public_id',queryset=MidUser.objects.all())
    created_at = CharFilter(method=filter_date)
    created_at__gte = CharFilter( method=filter_date)
    created_at__lte = CharFilter( method=filter_date)
    updated_at = CharFilter( method=filter_date)
    updated_at__gte = CharFilter(method=filter_date)
    updated_at__lte = CharFilter( method=filter_date)

    class Meta:
        model=Mymessage
        fields={
            'titel':['iexact'],
            'text':['icontains']
        }