from rest_framework import serializers
from .models import *
from apps.djalalidates.serializers import JalaliDateField
from apps.basicusers.models import BaseUser
class MyMessageSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='mymessages:message-detail',lookup_field='public_id',read_only=True)
    created_date=JalaliDateField(read_only=True)
    updated_date=JalaliDateField(read_only=True)
    read_date=JalaliDateField(read_only=True)
    sender=serializers.SerializerMethodField()
    reciver_url=serializers.SerializerMethodField()
    reciver=serializers.SlugRelatedField(queryset=BaseUser.objects.all(),slug_field='username')
    class Meta:
        model=Mymessage
        fields=['url','created_time','updated_time','created_date','updated_date','sender','reciver','reciver_url','text','titel','public_id'
                ,'read_status','read_date','read_time','created_time','updated_time']
        read_only_fields=('url','created_date','created_time','updated_time','updated_date','sender','reciver_url','public_id','read_status'
                          ,'read_date','read_time')
    
    def get_sender(self,obj):
        request=self.context.get('request')
        url_relative_address=f'/api/{obj.sender.role}'
        if obj.sender.role=='coach':
            url_relative_address+='es'
        else :
            url_relative_address+='s'
        url_relative_address+=f'/{obj.sender.public_id}'

        return request.build_absolute_uri(url_relative_address)

    def get_reciver_url(self,obj):
        request=self.context.get('request')
        url_relative_address=f'/api/{obj.reciver.role}'
        if obj.reciver.role=='coach':
            url_relative_address+='es'
        else :
            url_relative_address+='s'
        url_relative_address+=f'/{obj.reciver.public_id}'

        return request.build_absolute_uri(url_relative_address)
        