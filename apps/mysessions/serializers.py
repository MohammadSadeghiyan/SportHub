from .models import Mysession
from rest_framework import serializers

class MySessionSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='mysessions:session-detail',lookup_field='public_id',read_only=True)
    classes=serializers.HyperlinkedRelatedField(view_name='classes:class-detail',lookup_field='public_id',many=True,read_only=True)
    class Meta:
        model=Mysession
        fields=['url','name','start_time','end_time','days','public_id','classes','public_id']

    def validate(self, attrs):
        if attrs['end_time']<=attrs['start_time']:
            raise serializers.ValidationError({'time':'end time must be bigger than start time'})
        return attrs


