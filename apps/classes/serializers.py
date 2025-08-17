from rest_framework import serializers
from .models import Class
from apps.coaches.models import Coach
from apps.djalalidates.serializers import JalaliDateField
from django.utils import timezone

class ClassSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='classes:class-detail',lookup_field='public_id',read_only=True)
    reserves=serializers.HyperlinkedRelatedField(view_name='reservations:reserve-detail',lookup_field='public_id',read_only=True)
    coach=serializers.SlugRelatedField(slug_field='username',queryset=Coach.objects.all())
    coach_url=serializers.HyperlinkedRelatedField(source='coach',view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)
    start_date=JalaliDateField()
    end_date=JalaliDateField()
   
    class Meta:
        model=Class
        fields='__all__'
        read_only_fields=('url','status','class_salary_get_per_athlete_rial')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request=self.context.get('request')
        user=request.user
        if user.role=='coach':
            self.fields['coach'].read_only=True
            self.fields['coach'].read_only=True

    def validate_start_date(self,value):
        if value<timezone.now().date():
            raise serializers.ValidationError({'start_date':'start_date must be bigger than now time'})
        return value


    
