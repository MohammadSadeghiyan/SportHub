from .helpers import validate_iran_home_phone
from rest_framework import serializers
from .models import MidUser

class MidUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,write_only=True)
    send_messages=serializers.HyperlinkedRelatedField(view_name='messages:message-detail',lookup_field='public_id'
                                                      ,read_only=True,many=True)
    recived_messages=serializers.HyperlinkedRelatedField(view_name='messages:message-detail',lookup_field='public_id',
                                                         many=True,read_only=True)
    work_histories=serializers.HyperlinkedRelatedField(view_name='workhistories:workhistory-detail',lookup_field='public_id',
                                                       many=True,read_only=True)
    memberships=serializers.HyperlinkedRelatedField(read_only=True,view_name='memberships:membership-detail',many=True
                                                        ,lookup_field='public_id')
    orders=serializers.HyperlinkedRelatedField(view_name='orders:order-detail',lookup_field='public_id',many=True,read_only=True)
    payments=serializers.HyperlinkedRelatedField(view_name='payments:payment-detail',lookup_field='public_id',many=True,read_only=True)
    reserve_requests=serializers.HyperlinkedRelatedField(view_name='reservations:reservation-detail',read_only=True,many=True,
                                                         lookup_field='public_id')
    class Meta:
        model=MidUser
        fields=['public_id','username','password','role',
                'home_address','phone_number',
                'home_number','father_name','age',
                'balance_rial','status','image',
                'send_messages','recived_messages','work_histories'
                ,'memberships','orders','payments','reserve_requests']
        read_only_fields = ('public_id','status','role')

    def validate_home_number(self,value):
        validate_iran_home_phone(value)
        return value
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if instance.role=='receptionist':
            rep.pop('memberships')
            rep.pop('orders')
            rep.pop('payments')
        elif instance.role=='athlete':rep.pop('work_histories')
        elif instance.role=='coach':rep.pop('reserve_requests')
        return rep


        