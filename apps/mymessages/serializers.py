from rest_framework import serializers
from .models import *
from apps.djalalidates.serializers import JalaliDateField
from apps.basicusers.models import MidUser
class MyMessageSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='mymessages:message-detail',lookup_field='public_id',read_only=True)
    created_at=JalaliDateField(read_only=True)
    updated_at=JalaliDateField(read_only=True)
    sender=serializers.SerializerMethodField()
    reciver_url=serializers.SerializerMethodField()
    reciver=serializers.SlugRelatedField(queryset=MidUser.objects.all(),slug_field='username')
    class Meta:
        model=Mymessage
        fields=['url','created_at','updated_at','sender','reciver','reciver_url','text','titel']

    
    def get_sender(self,obj):
        request=self.context.get('request')
        return {'sender':request.build_absolute_uri(f'/api/{obj.sender.role}/{obj.sender.public_id}')}

    def get_reciver_url(self,obj):
        request=self.context.get('request')
        return {'sender':request.build_absolute_uri(f'/api/{obj.reciver.role}/{obj.reciver.public_id}')}
        