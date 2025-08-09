from rest_framework import serializers
from .models import Manager
from rest_framework_nested.relations import NestedHyperlinkedRelatedField
class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='manager-detail',lookup_field='public_id',read_only=True)
    reports=NestedHyperlinkedRelatedField(view_name='manager-reports-detail',lookup_field='public_id',many=True,read_only=True
                                            ,parent_lookup_kwargs={'manager_public_id':'manager__public_id'})
    password=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model=Manager
        fields=['url','username','password','role','reports']
        read_only_fields=('role','reports')


    
    def create(self, validated_data):
        password=validated_data.pop('password')
        user=Manager(**validated_data,role='manager')
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
