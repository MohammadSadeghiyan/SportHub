from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from apps.djalalidates.filters import filter_date
from .models import *
from apps.mysessions.models import Mysession

class ClassFilter(FilterSet):
    session=ModelChoiceFilter(field_name='session__public_id',queryset=Mysession.objects.all())
    coach=ModelChoiceFilter('coach__public_id',queryset=Coach.objects.all())
    days = CharFilter(method='filter_days')
    days__contains = CharFilter(method='filter_days_contains', lookup_expr='contains')
    end_date = CharFilter(method=filter_date)
    end_date__gte = CharFilter( method=filter_date)
    end_date__lte = CharFilter( method=filter_date)
    start_date = CharFilter( method=filter_date)
    start_date__gte = CharFilter(method=filter_date)
    start_date__lte = CharFilter( method=filter_date)

    

    def filter_days_contains(self, queryset, name, value):
        days = [day.strip() for day in value.split(',') if day.strip()]
        query = queryset
        for day in days:
            query = query.filter(days__contains=[day])
        return query
    
    def filter_days(self, queryset, name, value):
        return queryset.filter(days__contains=[value])
    class Meta:
        model=Class
        fields={
            'name':['iexact','icontains'],
            'class_salary_get_per_athlete_rial':['range','exact'],
            'end_time':['exact','lte','gte'],
            'start_time':['exact','lte','gte'],
            'capacity':['exact','range'],
        
        }