from rest_framework import serializers
from .models import Athlete
from apps.basicusers.serializers import MidUserSerializer

class AthleteSerializer(MidUserSerializer,serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='athletes:athlete-detail',lookup_field='public_id',read_only=True)
    reserves=serializers.HyperlinkedRelatedField(view_name='reservations:reserve-detail',lookup_field='public_id',read_only=True,many=True)
    sport_histories=serializers.HyperlinkedRelatedField(view_name='sporthistories:sport-history-detail',lookup_field='public_id'
                                                        ,read_only=True,many=True)
    class Meta(MidUserSerializer.Meta):
        model=Athlete
        fields=MidUserSerializer.Meta.fields+['url','sport_histories','reserves','weight','height']
        read_only_fields=MidUserSerializer.Meta.read_only_fields+('sport_history','reserves')


    def create(self, validated_data):
        password=validated_data.pop('password')
        user=Athlete(**validated_data,role='coach')
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
                
                
        if password:
            instance.set_password(password)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class PublicAthleteSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='athletes:athlete-detail',lookup_field='public_id',read_only=True)
    class Meta:
        model=Athlete
        fields=['url','status','username','weight','height','image']
        read_only_fields=('url','status','username','weight','height','image')