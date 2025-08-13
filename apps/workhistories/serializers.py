from rest_framework import serializers
from .models import *
from apps.receptionists.models import Receptionist
from apps.djalalidates.serializers import JalaliDateField
from apps.coaches.models import Coach


class WorkHistorySerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='workhistories:workhsitory-detail',lookup_field='public_id',read_only=True)
    user_url=serializers.SerializerMethodField()
    start_activity=JalaliDateField()
    end_activity=JalaliDateField()
    class Meta:
        model=WorkHistory
        fields=['url','user_url']+[f.name for f in WorkHistory._meta.get_fields() if f.name not in ['id','user']]

    def get_user(self,obj):
        request=self.context.get('request')
        if obj.user.role=='receptionist':
            return {'user':request.build_absolute_uri(f'/api/receptionist/{obj.user.public_id}')}
        else : return {'user':request.build_absolute_uri(f'/api/coaches/{obj.user.public_id}')}

class ReceptionistWorkHistorySerializer(WorkHistorySerializer):
    user=serializers.SlugRelatedField(slug_field='public_id',queryset=Receptionist.objects.all())

    class Meta(WorkHistorySerializer.Meta):
        fields=WorkHistorySerializer.Meta.fields+['user']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role=='receptionist':
            self.fields['user'].read_only=True
    


class CoachWorkHistorySerializer(WorkHistorySerializer):
    user=serializers.SlugRelatedField(slug_field='public_id',queryset=Coach.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user=self.context.get('request').user
        if user.role=='coach':
            self.fields['user'].read_only=True
        

    class Meta(WorkHistorySerializer.Meta):
        fields=WorkHistorySerializer.Meta.fields+['user']





