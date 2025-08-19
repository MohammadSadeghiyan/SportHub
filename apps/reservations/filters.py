from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from apps.djalalidates.filters import filter_date
from .models import *
from apps.classes.models import Class
from apps.basicusers.models import MidUser
from apps.athletes.models import Athlete
from .models import Reservation
class ReservationFilter(FilterSet):
    athlete=ModelChoiceFilter(field_name='athlete__public_id',queryset=Athlete.objects.all())
    class_ref=ModelChoiceFilter(field_name='class__public_id',queryset=Class.objects.all())
    reserved_by=ModelChoiceFilter(field_name='reserved_by__public_id',queryset=MidUser.objects.all())
    date = CharFilter(method=filter_date)
    date__gte = CharFilter( method=filter_date)
    date__lte = CharFilter( method=filter_date)
    registered_date = CharFilter( method=filter_date)
    registered__gte = CharFilter(method=filter_date)
    registered__lte = CharFilter( method=filter_date)

    

   
    class Meta:
        model=Reservation
        fields={
            'salary_rial':['exact','range'],
            'status':['exact'],

        
        }