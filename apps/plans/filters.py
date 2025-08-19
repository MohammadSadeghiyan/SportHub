from django_filters import FilterSet,ModelChoiceFilter
from .models import *
from apps.athletes.models import Athlete
from apps.djalalidates.filters import filter_date 
from django_filters import CharFilter
class PlanFilter(FilterSet):
    athlete=ModelChoiceFilter(field_name='athlete__public_id',queryset=Athlete.objects.all())
    coach=ModelChoiceFilter(field_name='coach__public_id',queryset=Coach.objects.all())
    end_date = CharFilter(method=filter_date)
    end_date__gte = CharFilter( method=filter_date)
    end_date__lte = CharFilter( method=filter_date)
    start_date = CharFilter( method=filter_date)
    start_date__gte = CharFilter(method=filter_date)
    start_date__lte = CharFilter( method=filter_date)
    created_at = CharFilter(method=filter_date)
    created_at__gte = CharFilter( method=filter_date)
    created_at__lte = CharFilter( method=filter_date)
    registered_at = CharFilter( method=filter_date)
    registered_at__gte = CharFilter(method=filter_date)
    registered_at__lte = CharFilter( method=filter_date)

    class Meta:
        model=NutritionPlan
        fields={
            'status':['exact'],
            'name':['iexact'],
            'description':['icontains'],
            'salary_rial':['range','exact']

        }


