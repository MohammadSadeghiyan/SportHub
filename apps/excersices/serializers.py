from rest_framework import serializers
from .models import *
from apps.sporthistories.models import SportHistory
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
class ExcersiceHistorySerializer(serializers.ModelSerializer):
    excersice=serializers.SlugRelatedField(queryset=Excersice.objects.all(),slug_field='public_id')
    class Meta:
        model =Excersice_history
        fields='__all__'   
    
    def validate_excersice(self,value):
        user=self.context.get('request').user
        if value.sport_history.athlete.public_id==user.public_id:
            return value
        raise serializers.ValidationError({'excersice':'this excersice isnt for you'})

class ExcersiceSerializer(serializers.ModelSerializer):
    sport_history=serializers.SlugRelatedField(queryset=SportHistory.objects.all(),slug_field='public_id')
    excersice_history=serializers.SerializerMethodField()
    class Meta:
        model=Excersice
        fields=[f.name for f in Excersice._meta.get_fields() if f.name!='id']+['excersice_history']
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role=='coach':
            self.fields['status'].read_only=True
            if self.context.get('request').method in ['PUT',"PATCH"]:
                self.fields['sport_history'].read_only=True
        
        if user.role=='athlete':
            self.fields['sport_history'].read_only=True
            self.fields['start_date'].read_only=True
            self.fields['end_date'].read_only=True
            self.fields['description'].read_only=True
    
    def validate(self, data):
        if data['sport_history'] and data['name']:
            sport_history=data['sport_history']
            name=data['name']
        else:
            sport_history=data['sport_history'] if data['sport_history']else self.instance.sport_history
            name=data['name']if data['name'] else self.instance.name

        if Excersice.objects.filter(sport_history=sport_history,name=name).exists():
            raise serializers.ValidationError({'sport_history name':'then name in the specific sport history must be unique'})
        return data
    
    def validate_sport_history(self,value):
        user=self.context.get('request').user
        if value.coach.public_id==user.public_id:
            return value
        raise serializers.ValidationError({'access':'you dont have access to the sporthistory that your arent that coach'})
    @extend_schema_field(OpenApiTypes.ANY)
    def get_excersice_history(self,obj):
        request=self.context.get('request')
        include=request.query_params.get('include','')
        if 'history' in include:
            histories=obj.excersice_history.all()
            return ExcersiceHistorySerializer(histories,many=True).data
        return {
            'excersice_history':[
                request.build_absolute_uri(f'/api/excersice-histories/{history.public_id}')
                for history in obj.excersice_history.all()
            ]
        }

