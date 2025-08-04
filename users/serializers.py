from rest_framework import serializers
from .models import *
class ManagerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Manager
        fields=['username','password','role']

class ReseptionSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='',pk='pk',
                                             read_only=True)
    class Meta:
        model=Reseption
        fields=['url','username','password','role']
        read_only_fields=('role')

    def __init__(self, args,**kwargs):
        super().__init__( args, **kwargs)
        request=self.context['request']
        user=request.user
        
        if request.method in ['PUT','PATCH']:
            self.fields['password'].required=False
        
        
        if user.role=='manager' or user.is_superuser:
            self.fields['role'].read_only=False


class AthleteSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='',pk='pk',read_only=True)
    reserves=serializers.HyperlinkedRelatedField(view_name='',pk='pk',read_only=True,many=True)
    class Meta:
        model=Athlete
        fields=['url','username','password','sport_history','reserves','wieght','hieght']


