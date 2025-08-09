from rest_framework import serializers
from .models import Manager

class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='users:manager-detail',read_only=True)
    password=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model=Manager
        fields=['url','username','password','role']
        read_only_fields=('role',)


    
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
