from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.mysessions.models import Mysession
from apps.classes.models import Class

class MySessionFilter(FilterSet):
    classes=ModelChoiceFilter(field_name='classes__public_id',queryset=Class.objects.all())
    days = CharFilter(method='filter_days')
    days__contains = CharFilter(method='filter_days_contains', lookup_expr='contains')
    

    def filter_days_contains(self, queryset, name, value):
        days = [day.strip() for day in value.split(',') if day.strip()]
        query = queryset
        for day in days:
            query = query.filter(days__contains=[day])
        return query
    
    def filter_days(self, queryset, name, value):
        return queryset.filter(days__contains=[value])
    class Meta:
        model=Mysession
        fields={
            'name':['iexact','icontains'],
            'end_time':['exact','lte','gte'],
            'start_time':['exact','lte','gte'],
        
        }