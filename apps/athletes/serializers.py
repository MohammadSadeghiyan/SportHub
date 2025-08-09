from rest_framework import serializers
from .models import Athlete
from apps.basicusers.serializers import MidUserSerializer

class AthleteSerializer(MidUserSerializer,serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='users:athlete-detail',read_only=True)
    reserves=serializers.HyperlinkedRelatedField(view_name='reservations:reserve-detail',read_only=True,many=True)
    sporthistory=serializers.HyperlinkedRelatedField(view_name='sporthistories:sporthistory-detail',read_only=True,many=True)
    class Meta(MidUserSerializer.Meta):
        model=Athlete
        fields=MidUserSerializer.Meta.fields+['url','sport_history','reserves','weight','height']
        read_only_fields=('sport_history','reserves')


