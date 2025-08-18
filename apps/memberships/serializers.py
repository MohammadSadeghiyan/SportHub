from .models import Membership
from rest_framework import serializers
from apps.djalalidates.serializers import JalaliDateField
from django.utils import timezone
from apps.coaches.models import Coach
from apps.athletes.models import Athlete


class AbstractMembershipSerializer(serializers.ModelSerializer):
    start_date=JalaliDateField()
    end_date=JalaliDateField(read_only=True)
    class Meta:
        model=Membership
        fields=['start_date','end_date','type_name','status','user','membership_cost_rial']
        read_only_fields=('end_date','status','user','membership_cost_rial')

    
    
    def validate_start_date(self,value):
        if value>timezone.now().date():
            raise serializers.ValidationError({'start_date':'start date must be bigger than now '})


class CoachMembershipSerializer(serializers.HyperlinkedModelSerializer,AbstractMembershipSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='memberships:coach-membership-detail',lookup_field='public_id',read_only=True)

    user=serializers.SlugRelatedField(slug_field='username',queryset=Coach.objects.all())
    user_url=serializers.HyperlinkedRelatedField(source='user',view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)

    class Meta(AbstractMembershipSerializer.Meta):
        fields=AbstractMembershipSerializer.Meta.fields+['url','user_url','user']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role=='coach':
            self.fields['user'].read_only=True

class AthleteMembershipSerializer(serializers.HyperlinkedModelSerializer,AbstractMembershipSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='memberships:athlete-membership-detail',lookup_field='public_id',read_only=True)

    user=serializers.SlugRelatedField(slug_field='username',queryset=Athlete.objects.all())

    user_url=serializers.HyperlinkedRelatedField(source='user',view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)

    class Meta(AbstractMembershipSerializer.Meta):
        fields=AbstractMembershipSerializer.Meta.fields+['url','user_url','user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role=='athlete':
            self.fields['user'].read_only=True