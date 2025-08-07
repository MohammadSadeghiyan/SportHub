from rest_framework import serializers
from .models import *
class ManagerSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='users:manager-detail',lookup_field='pk',read_only=True)
    password=serializers.CharField(max_length=255,write_only=True)
    reports=serializers.HyperlinkedRelatedField(many=True,view_name='reports:report-detail',lookup_field='pk',read_only=True)
    class Meta:
        model=Manager
        fields=['url','username','password','role','reports']
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

class MidUserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,write_only=True)
    class Meta:
        model=MidUser
        fields=['username','password','role',
                'home_address','phone_number',
                'father_name','age','image',
                'balance_rial','status']
        read_only_fields = ('status','role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request=self.context.get('request')
        user=request.user
        if request.method in ['PUT','PATCH']:
            self.fields['password'].required=False


# class ReseptionSerializer(serializers.HyperlinkedModelSerializer):
#     url=serializers.HyperlinkedIdentityField(view_name='',lookup_field='pk',
#                                              read_only=True)
#     user=MidUserSerializer()
#     class Meta:
#         model=Receptionist
#         fields=['url','user']
        
        
        

#     def create(self, validated_data):
#         request=self.context.get('request')
#         user=request.user
#         user_data=validated_data.pop('user')
#         password=user_data.pop('password')
#         user=Receptionist(**user_data)
#         user.set_password(password)
#         user.save()
#         return user
    
#     def update(self, instance, validated_data):
#         user_data=validated_data.pop('user')
#         password = validated_data.pop('password', None)
#         if password is not None:
#             instance.set_password(password)
            
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()
#         return instance

# class AthleteSerializer(serializers.HyperlinkedModelSerializer):
#     url=serializers.HyperlinkedIdentityField(view_name='',lookup_field='pk',read_only=True)
#     reserves=serializers.HyperlinkedRelatedField(view_name='',lookup_field='pk',read_only=True,many=True)
#     class Meta:
#         model=Athlete
#         fields=['url','username','password','sport_history','reserves','wieght','hieght']


