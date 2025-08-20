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
        if value in ['athlete','coach']:
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


class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()


class RequestPasswordEmailSerializer(serializers.Serializer):
    email=serializers.EmailField()

    class Meta:
        fields=['email']


    def validate_email(self, value):
        email=value
        if MidUser.objects.filter(email=email).exists():
            return value
        raise serializers.ValidationError({"email":'email is not true'})
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data