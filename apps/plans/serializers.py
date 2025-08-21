from .models import NutritionPlan,Meal
from rest_framework import serializers
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
from apps.djalalidates.serializers import JalaliDateField
from django.utils import timezone
class NutritionPlanSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='plans:nutritionplan-detail',lookup_field='public_id',read_only=True)
    athlete=serializers.SlugRelatedField(queryset=Athlete.objects.all(),slug_field='username')
    coach=serializers.SlugRelatedField(slug_field='username',queryset=Coach.objects.all())
    athlete_url=serializers.HyperlinkedRelatedField(view_name='athletes:athlete-detail',lookup_field='public_id',read_only=True)
    coach_url=serializers.HyperlinkedRelatedField(view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)
    start_date=JalaliDateField()
    end_date=JalaliDateField()
    created_at=JalaliDateField(read_only=True)
    registered_at=JalaliDateField(read_only=True)
    class Meta:
        model=NutritionPlan
        fields=['url','athlete','coach','athlete_url','coach_url','name','public_id','description','status','confirmation_coach',
                'start_date','end_date','salary_rial','created_at','registered_at']
        read_only_fields=('url','athlete_url','coach_url','public_id','status','created_at','registered_at','salary_rial')

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role!='coach':
            self.fields['confirmation_coach'].read_only=True
        if user.role=='athlete':
            self.fields['athlete'].read_only=True
            self.fields['description'].read_only=True
        elif user.role=='coach':
            self.fields['coach'].read_only=True
            self.fields['athlete'].read_only=True
            self.fields['start_date'].read_only=True
            self.fields['end_date'].read_only=True

    
    def validate(self, attrs):
        end_date=attrs.get('end_date') if attrs.get('end_date',None) else self.instance.end_date
        start_date=attrs.get('start_date',None) if attrs.get('start_date',None) else self.instance.start_date
        if end_date<start_date:
            raise serializers.ValidationError({'end date':'end date must be bigger than end date'})
        return attrs
    
    def validate_start_date(self,value):
        if value<timezone.now().date():
            raise serializers.ValidationError({'start date':'start date must be bigger than now'})
        return value
    


class MealSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plans:meal-detail',
        lookup_field='public_id',  
        read_only=True
    )
    nutrition_plan=serializers.SlugRelatedField(queryset=NutritionPlan.objects.all(),slug_field='public_id')
    athlete_date_done = JalaliDateField(read_only=True)
    nutrition_plan_url = serializers.HyperlinkedRelatedField(
        source='nutrition_plan',
        view_name='plans:nutritionplan-detail',
        lookup_field='public_id',
        read_only=True
    )

    class Meta:
        model = Meal
        fields = [
            'url',
            'day',
            'meal_type',
            'nutrition_plan',
            'nutrition_plan_url',
            'url',
            'athlete_date_done',
            'meal_discription'
        ]

    
    def validate_nutrition_plan(self,value):
        nutrition_plan=NutritionPlan.objects.filter(public_id=value.public_id,athlete__public_id=self.context.get('request').user.public_id)
        if nutrition_plan.exists():
            return value
        else :
            raise serializers.ValidationError({'nutrition plan':'this plan isnot for you'})
