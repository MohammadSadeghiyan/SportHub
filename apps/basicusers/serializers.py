from .helpers import validate_iran_home_phone
from rest_framework import serializers
from .models import MidUser

class MidUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,write_only=True)
    send_messages=serializers.HyperlinkedRelatedField(view_name='users:message-detail',read_only=True,many=True)
    recived_messages=serializers.HyperlinkedRelatedField(view_name='users:message-detail',many=True,read_only=True)
    work_histories=serializers.HyperlinkedRelatedField(view_name='users:workhistories-detail',many=True,read_only=True)
    class Meta:
        model=MidUser
        fields=['username','password','role',
                'home_address','phone_number',
                'home_number','father_name','age',
                'balance_rial','status','image',
                'send_messages','recived_messages','work_histories']
        read_only_fields = ('status','role','send_messages','recived_messages','work_histories')

    def validate_home_number(self,value):
        validate_iran_home_phone(value)
        return value