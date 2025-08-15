from django_filters import FilterSet,ModelChoiceFilter,CharFilter
from .models import ClassItemPricing,MembershipPricing,AbstractPricing,SportHistoryPricing,NutritionPricing
from apps.djalalidates.filters import filter_date
from apps.mysessions.models import Mysession

class AbstractPricingFilter(FilterSet):
    end_start_date = CharFilter(method=filter_date)
    end_start_date__gte = CharFilter( method=filter_date)
    end_start_date__lte = CharFilter( method=filter_date)
    start_start_date = CharFilter( method=filter_date)
    start_start_date__gte = CharFilter(method=filter_date)
    start_start_date__lte = CharFilter( method=filter_date)

    class Meta:
        model=None
        fields={'gym_fee':['exact','range','gte','lte']}

class ClassItemPricingFilter(AbstractPricingFilter):
    session_ref=ModelChoiceFilter(field_name='session_ref__public_id',queryset=Mysession.objects.all())
    
    class Meta(AbstractPricingFilter.Meta):
        model=ClassItemPricing
        fields={
            **AbstractPricingFilter.Meta.fields,
            'public_id':['exact'],
            'max_capacity':['range','exact','gte','lte'],
            'min_capacity':['range','exact','lte','gte'],
            'price_per_hour':['range','exact','lte','gte']

        }


class MembershipPricingFilter(AbstractPricingFilter):
   

    class Meta(AbstractPricingFilter.Meta):
        model=MembershipPricing
        fields={
            **AbstractPricingFilter.Meta.fields,
            'type_name':['exact'],
            'price':['exact','range','gte','lte']

        }

class SportHistoryPricingFilter(AbstractPricingFilter):
    
    class Meta(AbstractPricingFilter.Meta):
        model=SportHistoryPricing
        fields={
            **AbstractPricingFilter.Meta.fields,
            'price_per_day':['exact','range','lte','gte']
        }


class NutritionPricingFilter(AbstractPricingFilter):
    
    class Meta(AbstractPricingFilter.Meta):
        model=NutritionPricing
        fields={
            **AbstractPricingFilter.Meta.fields,
            'price_per_day':['exact','range','lte','gte']
        }