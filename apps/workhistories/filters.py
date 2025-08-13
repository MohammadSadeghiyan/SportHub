from django_filters import FilterSet,ModelChoiceFilter
from .models import *

class WorkHistoryFilter(FilterSet):

    class Meta:
        model=WorkHistory
        fields={
            'activity_type':['iexact','icontains'],
            'activity_description':['icontains']
        }