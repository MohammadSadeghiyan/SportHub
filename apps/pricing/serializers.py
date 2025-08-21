from rest_framework import serializers
from .models import *
from apps.djalalidates.helpers import start_date_validator
from apps.djalalidates.serializers import JalaliDateField
from apps.mysessions.models import Mysession
class AbstractPricingSerializer(serializers.ModelSerializer):
    start_start_date=JalaliDateField()
    end_start_date=JalaliDateField()
    class Meta:
        model=AbstractPricing
        fields=[f.name for f in AbstractPricing._meta.get_fields() if f.name!='id']

    def validate_start_start_date(self,value):
        start_date_validator(value)
        return value
    
    def validate(self, data):
        start_start_date=data.get('start_start_date',self.instance.start_start_date)
        end_start_date=data.get('end_start_date',self.instance.end_start_date)
        if start_start_date>end_start_date:
            raise serializers.ValidationError({'end_start_date':'end start date must be bigger than start start date'})
        return data
        
   
class MembershipPricingSerializer(serializers.HyperlinkedModelSerializer,AbstractPricingSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='pricing:membershippricing-detail',lookup_field='public_id',read_only=True)

    class Meta:
        model=MembershipPricing
        fields='__all__'

class SportHistoryPricingSerializer(serializers.HyperlinkedModelSerializer,AbstractPricingSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='pricing:sporthistorypricing-detail',lookup_field='public_id',read_only=True)

    class Meta:
        model=SportHistoryPricing
        fields='__all__'

class NutritionPricingSerializer(serializers.HyperlinkedModelSerializer,AbstractPricingSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='pricing:nutritionpricing-detail',lookup_field='public_id',read_only=True)

    class Meta:
        model=NutritionPricing
        fields='__all__'


        


class ClassItemPricingSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='pricing:classitempricing-detail',lookup_field='public_id',read_only=True)
    pricing=serializers.HyperlinkedRelatedField(view_name='pricing:classpricing-detail',lookup_field='public_id',read_only=True)
    session_ref=serializers.SlugRelatedField(queryset=Mysession.objects.all(),slug_field='public_id')
    session_url=serializers.HyperlinkedRelatedField(view_name='mysession:mysession-detail',lookup_field='public_id'
                                                    ,read_only=True)
    start_start_date=JalaliDateField()
    end_start_date=JalaliDateField()
    class Meta:
       model=ClassItemPricing
       fields='__all__' 


    def validate_start_start_date(self,value):
        start_date_validator(value)
        return value
    
    def validate(self, data):
        start_start_date=data.get('start_start_date',self.instance.start_start_date)
        end_start_date=data.get('end_start_date',self.instance.end_start_date)
        if start_start_date>end_start_date:
            raise serializers.ValidationError({'end_start_date':'end start date must be bigger than start start date'})
        if data['max_capacity']<data['min_capacity']:
            raise serializers.ValidationError({'max_capacity':'max capacity must be bigger than min capacity'})
        return data

class ClassPricingSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='pricing:classpricing-detail',lookup_field='public_id',read_only=True)
    items=ClassItemPricingSerializer(many=True,required=True)

    class Meta:
        model=ClassPricing
        fields=['url','items']


    
 