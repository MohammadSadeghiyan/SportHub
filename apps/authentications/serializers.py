from rest_framework import serializers
from apps.basicusers.models import MidUser
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
from apps.receptionists.models import Receptionist
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=MidUser
        fields=['username','email','password','role']
        extra_kwargs = {
        'password': {'write_only': True}
    }

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.fields:
            self.fields[field].required=True

    def validate_role(self,value):
        if value in ['receptionist','athlete','coach']:
            return value
        raise serializers.ValidationError({'role':'role isnt true.'})
    
    def validate_email(self, value):
        if MidUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("emial is exist")
        return value


    def create(self, validated_data):
        password=validated_data.pop('password')
        if validated_data['role'] =='receptionist':
            user=Receptionist.objects.create_user(**validated_data,password=password)
        elif validated_data['role']=='coach':
            user=Coach.objects.create_user(**validated_data,password=password)
        else : user=Athlete.objects.create_user(**validated_data,password=password)   
        return user    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)