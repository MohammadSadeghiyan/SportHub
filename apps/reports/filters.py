from django_filters import FilterSet,CharFilter
from .models import *
from rest_framework.exceptions import ValidationError
from apps.djalalidates.filters import filter_date
class ReportFilter(FilterSet):

    end_date = CharFilter(method=filter_date)
    end_date__gte = CharFilter( method=filter_date)
    end_date__lte = CharFilter( method=filter_date)
    start_date = CharFilter( method=filter_date)
    start_date__gte = CharFilter(method=filter_date)
    start_date__lte = CharFilter( method=filter_date)
        


    class Meta:
        model=Report
        fields={
            'name':['iexact','icontains'],
            'type_name':['exact'],
        }