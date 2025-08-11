from django_filters import FilterSet,ModelChoiceFilter
from .models import *
from apps.sporthistories.models import SportHistory
class ExcersiceFilter(FilterSet):
    sport_history=ModelChoiceFilter(field_name='sport_history__public_id',queryset=SportHistory.objects.all())

    class Meta:
        model=Excersice
        fields={
            'status':['exact'],
            'name':['iexact','icontains'],
            'sport_history':['exact'],
            'end_date':['exact','gt','lt'],
            'start_date':['exact','gt','lt']
        }


class ExcersiceHistoryFilter(FilterSet):
    excersice=ModelChoiceFilter(field_name='excersice__public_id',queryset=Excersice.objects.all())
    class Meta:
        model=Excersice_history
        fields={
            'description':['icontains'],
            'excersice':['exact']
        }
