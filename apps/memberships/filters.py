from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.djalalidates.filters import filter_date

class MembershipFilter(FilterSet):
    user=ModelChoiceFilter(field_name='user__public_id',queryset=MidUser.objects.all())

    end_date = CharFilter(method=filter_date)
    end_date__gte = CharFilter( method=filter_date)
    end_date__lte = CharFilter( method=filter_date)
    start_date = CharFilter( method=filter_date)
    start_date__gte = CharFilter(method=filter_date)
    start_date__lte = CharFilter( method=filter_date)

    class Meta:
        model=Membership
        fields={
            'type_name':['exact'],
            'status':['exact'],
            'membership_cost_rial':['range','exact']
        }