from django_filters import FilterSet,ModelChoiceFilter
from .models import *

class ReportFilter(FilterSet):

    class Meta:
        models=Report
        fields={
            'name':['iexact','icontains'],
            'type_name':['iexact','icontains'],
            'end_date':['exact','gte','lte'],
            'start_date':['exact','gte','lte']
        }