from django_filters import FilterSet
from .models import *

class AthleteFilter(FilterSet):

    class Meta:
        model=Athlete
        fields={
            'username':['exact','iexact','icontains'],
            'status':['exact'],
            'age':['exact','gte','lte'],
            'weight':['exact','range'],
            'height':['exact','range']
        }