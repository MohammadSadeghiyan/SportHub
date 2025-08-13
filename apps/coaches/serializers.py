from rest_framework import serializers
from .models import Coach
from apps.basicusers.serializers import MidUserSerializer
from apps.sporthistories.models import SportHistory
from django.utils import timezone
class PublicCoachSerializer(serializers.HyperlinkedModelSerializer,MidUserSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)
    classes=serializers.HyperlinkedRelatedField(read_only=True,lookup_field='public_id'
                                                ,view_name='classes:class-detail',many=True)
    active_athletes_number=serializers.SerializerMethodField()
    all_athletes_number=serializers.SerializerMethodField()

    def get_active_athletes_number(self,obj):
        count=SportHistory.objects.filter(coach=obj,confirmation_coach=True,end_date__gt=timezone.now().date())\
                                    .select_related('athlete').only('athlete__public_id').distinct().count()
        return count

    def get_all_athletes_number(self,obj):
        count=SportHistory.objects.filter(coach=obj,confirmation_coach=True).select_related('athlete')\
                                .only('athlete__public_id').distinct().count()

        return count
    
    
    class Meta(MidUserSerializer.Meta):
        model = Coach
        fields=['url']+[f for f in MidUserSerializer.Meta.fields if f not in['home_address','phone_number','home_number','father_name',
                    'balance_rial']]+['classes','active_athletes_number','all_athletes_number']

class CoachSerializer(serializers.HyperlinkedModelSerializer,MidUserSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)
    work_histories=serializers.HyperlinkedRelatedField(view_name='workhistories:coach-workhistory-detail',lookup_field='public_id',
                                                       many=True,read_only=True)
    classes=serializers.HyperlinkedRelatedField(read_only=True,lookup_field='public_id'
                                                ,view_name='classes:class-detail',many=True)
    athletes=serializers.HyperlinkedRelatedField(view_name='athletes:athlete-detail'
                                                 ,lookup_field='public_id',many=True,read_only=True)
    sport_histories=serializers.HyperlinkedRelatedField(view_name='sporthistories:sporthistory-detail'
                                                        ,lookup_field='public_id',read_only=True,many=True)
    class Meta(MidUserSerializer.Meta):
        model = Coach
        fields=['url']+MidUserSerializer.Meta.fields+['classes','athletes','sport_histories','work_histories']

    def create(self, validated_data):
        password=validated_data.pop('password')
        user=Coach(**validated_data,role='coach')
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
    

        

    
       