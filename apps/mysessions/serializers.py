from .models import Mysession
from rest_framework import serializers

class MySessionSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='mysessions:session-detail',lookup_field='public_id',read_only=True)
    classes=serializers.HyperlinkedRelatedField(view_name='classes:class-detail',lookup_field='public_id',many=True,read_only=True)
    class Meta:
        model=Mysession
        fields=['url','name','start_time','end_time','days','public_id','classes','public_id']

    def validate(self, attrs):
        start_time=attrs.get('start_time')if attrs.get('start_time',None) else self.instance.start_time
        end_time=attrs.get('end_time')if attrs.get('end_time',None) else self.instance.end_time
        if start_time>end_time:
            raise serializers.ValidationError({'time':'end time must be bigger than start time'})
        return attrs


