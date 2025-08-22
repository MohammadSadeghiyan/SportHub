from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import *
from apps.djalalidates.filters import filter_date
from apps.basicusers.models import MidUser
from apps.athletes.models import Athlete

class OrderFilter(FilterSet):
    user=ModelChoiceFilter(field_name='user__public_id',queryset=MidUser.objects.all())
    created_at = CharFilter(method=filter_date)
    created_at__lte = CharFilter( method=filter_date)
    created_at__gte= CharFilter( method=filter_date)
    updated_at = CharFilter( method=filter_date)
    updated_at__gte = CharFilter(method=filter_date)
    updated_at__lte = CharFilter( method=filter_date)

    class Meta:
        model=Order
        fields={
            'price':['range','exact'],
            'status':['exact']
        }


class MembershipItemFilter(FilterSet):
    user=ModelChoiceFilter(field_name='order__user__public_id',queryset=MidUser.objects.all())


    class Meta:
        model=MembershipItem
        fields={
            'price':['range','exact'],
        }


class SportHistoryItemFilter(FilterSet):
    athlete=ModelChoiceFilter(field_name='order__user__public_id',queryset=Athlete.objects.all())

    class Meta:
        model=SportHistoryItem
        fields={
            'price':['range','exact'],
        }


class NutritionPlanItemFilter(FilterSet):
    user=ModelChoiceFilter(field_name='order__user__public_id',queryset=Athlete.objects.all())

    class Meta:
        model=NutritionPlanItem
        fields={
            'price':['range','exact'],
        }


class ReservationItemFilter(FilterSet):
    user=ModelChoiceFilter(field_name='order__user__public_id',queryset=Athlete.objects.all())

    class Meta:
        model=ReservationItem
        fields={
            'price':['range','exact'],
        }


