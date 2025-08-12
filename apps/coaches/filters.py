from django_filters import FilterSet,ModelChoiceFilter
from .models import *

class CoachFilter(FilterSet):

    class Meta:
        model=Coach
        fields={
            'username':['exact','iexact','icontains'],
            'status':['exact'],
            'age':['exact','gte','lte'],
        }