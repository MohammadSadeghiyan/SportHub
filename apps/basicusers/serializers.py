from .helpers import validate_iran_home_phone
from rest_framework import serializers
from .models import MidUser
from apps.djalalidates.serializers import JalaliDateField
class MidUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,write_only=True)
    memberships=serializers.HyperlinkedRelatedField(read_only=True,view_name='memberships:membership-detail',many=True
                                                        ,lookup_field='public_id')
    status=serializers.CharField(source='get_status_display',read_only=True)
    date_joined=JalaliDateField()
    class Meta:
        model=MidUser
        fields=['public_id','username','password','role','memberships',
                'home_address','phone_number',
                'home_number','father_name','age',
                'balance_rial','status','image']
        read_only_fields = ('date_joined','public_id','status','role','balance_rial')

    def validate_home_number(self,value):
        validate_iran_home_phone(value)
        return value
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if instance.role=='receptionist':rep.pop('memberships')
        return rep

        