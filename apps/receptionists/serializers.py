from apps.basicusers.serializers import MidUserSerializer
from rest_framework import serializers
from .models import Receptionist


class ReceptionistSerializer(MidUserSerializer,serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='receptionists:receptionist-detail',read_only=True)
    work_histories=serializers.HyperlinkedRelatedField(view_name='workhistories:receptionist-workhistory-detail'
                                                       ,lookup_field='public_id',many=True,read_only=True)
    specific_payments=serializers.HyperlinkedRelatedField(view_name='payments:specificpayments-detail',
                                                            lookup_field='pbulic_id',many=True,read_only=True)
    reserve_requests=serializers.HyperlinkedRelatedField(view_name='reservations:reserve-detail',lookup_field='public_id'
                                                         ,many=True,read_only=True)
    class Meta(MidUserSerializer.Meta):
        model=Receptionist
        fields=MidUserSerializer.Meta.fields+['url','specific_payments','reserve_requests','work_histories']


    def create(self, validated_data):
        password=validated_data.pop('password')
        receptionist=Receptionist(**validated_data,role='receptionist')
        receptionist.set_password(password)
        receptionist.save()
        return receptionist
        
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.role='receptionist'
        instance.save()
        return instance