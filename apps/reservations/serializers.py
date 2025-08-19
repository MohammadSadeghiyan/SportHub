from rest_framework import serializers
from .models import Reservation
from apps.classes.models import Class
from apps.djalalidates.serializers import JalaliDateField
from apps.athletes.models import Athlete
class ReservationSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='reservations:reservation-detail',lookup_field='public_id',read_only=True)
    class_ref=serializers.SlugRelatedField(queryset=Class.objects.all(),slug_field='public_id')
    class_url=serializers.HyperlinkedRelatedField(view_name='classes:class-detail',lookup_field='public_id',read_only=True)
    athlete=serializers.SlugRelatedField(queryset=Athlete.objects.all(),slug_field='username')
    athlete_url=serializers.HyperlinkedRelatedField(view_name='athletes:athlete-detail',lookup_field='public_id',read_only=True)
    date=JalaliDateField(read_only=True)
    reserved_by=serializers.SerializerMethodField()
    registered_date=JalaliDateField(read_only=True)
    class Meta:
        model=Reservation
        fields=['url','public_id','class_ref','class_url','athlete','athlete_url','salary_rial','status','date'
                ,'reserved_by','registered_date']
        read_only_fields=('salary_rial','athlete','status')
        extra_kwargs = {
        'class_ref': {'write_only': True},
        'athlete':{'write_only':True}
    }
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].user.role=='athlete':
            self.fields['athlete'].read_only=True
            
    def get_reserved_by(self,obj):
        request=self.context.get('request')
        return {'url':request.build_absolute_uri(f'/api/{obj.reserved_by.role}s/{obj.reserved_by.public_id}')}