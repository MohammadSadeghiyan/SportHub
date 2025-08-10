from rest_framework import serializers
from .models import *
from apps.sporthistories.models import SportHistory
from drf_spectacular.utils import extend_schema_field
class ExcersiceHistorySerializer(serializers.ModelSerializer):
    excersice=serializers.SlugRelatedField(slug_field='public_id',
                                           qeuryset=Excersice.objects.all())
    class Meta:
        model =Excersice_history
        fields='__all__'   
    
    def validate_excersice(self,value):
        user=self.context.get('request').user
        if value.sport_history.athlete.public_id==user.public_id:
            return value
        raise serializers.ValidationError({'excersice':'this excersice isnt for you'})

class ExcersiceSerializer(serializers.ModelSerializer):
    sport_history=serializers.SlugRelatedField(slug_field='public_id',queryset=SportHistory.objects.all())
    excersice_history=serializers.SerializerMethodField()
    class Meta:
        model=Excersice
        fields=[f.name for f in Excersice._meta.get_fields() if f.name!='id']+['excersce_history']
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role=='coach':
            self.fields['status'].read_only=True
        
        if user.role=='athlete':
            self.fields['sport_history'].read_only=True
            self.fields['start_date'].read_only=True
            self.fields['end_date'].read_only=True
            self.fields['description'].read_only=True

    def validate_sport_history(self,value):
        user=self.context.get('request').user
        if value.coach.public_id==user.public_id:
            return value
        raise serializers.ValidationError({'access':'you dont have access to the sporthistory that your arent that coach'})
    
    @extend_schema_field(ExcersiceHistorySerializer(many=True))
    def get_excersice_history(self,obj):
        request=self.context.get('request')
        include=request.query_params.get('include','')
        if 'history' in include:
            histories=obj.excersice_history.all().select_related('excersice')
            return ExcersiceHistorySerializer(histories,many=True).data
        return {
            'excersice_history':[
                request.build_absolute_uri(f'/api/excersice-histories/{history.public_id}')
                for history in obj.excersice_history.all()
            ]
        }

