from django_filters import FilterSet,ModelChoiceFilter
from .models import *
from apps.sporthistories.models import SportHistory
from apps.djalalidates.filters import filter_date 
from django_filters import CharFilter
class ExcersiceFilter(FilterSet):
    sport_history=ModelChoiceFilter(field_name='sport_history__public_id',queryset=SportHistory.objects.all())
    end_date = CharFilter(method=filter_date)
    end_date__gte = CharFilter( method=filter_date)
    end_date__lte = CharFilter( method=filter_date)
    start_date = CharFilter( method=filter_date)
    start_date__gte = CharFilter(method=filter_date)
    start_date__lte = CharFilter( method=filter_date)

    class Meta:
        model=Excersice
        fields={
            'status':['exact'],
            'name':['iexact','icontains'],
        }


class ExcersiceHistoryFilter(FilterSet):
    excersice=ModelChoiceFilter(field_name='excersice__public_id',queryset=Excersice.objects.all())
    class Meta:
        model=Excersice_history
        fields={
            'description':['icontains'],
        }
