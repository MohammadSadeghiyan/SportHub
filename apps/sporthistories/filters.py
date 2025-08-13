from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.coaches.models import Coach
from apps.djalalidates.filters import filter_date
from apps.athletes.models import Athlete

class SportHistoryFilter(FilterSet):
    coach=ModelChoiceFilter(field_name='coach__public_id',queryset=Coach.objects.all())
    athlete=ModelChoiceFilter(field_name='athlete__public_id',queryset=Athlete.objects.all())
    end_date = CharFilter(method=filter_date)
    end_date__gte = CharFilter( method=filter_date)
    end_date__lte = CharFilter( method=filter_date)
    start_date = CharFilter( method=filter_date)
    start_date__gte = CharFilter(method=filter_date)
    start_date__lte = CharFilter( method=filter_date)
    class Meta:
        model=SportHistory
        fields={
            'confirmation_coach':['exact'],
            'balance_for_coaching_rial':['exact','gte','lte','range'],
            'status':['exact']
        }