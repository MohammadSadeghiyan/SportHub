from rest_framework import serializers
from .models import Coach
from apps.basicusers.serializers import MidUserSerializer

class CoachSerializer(MidUserSerializer):
    classes=serializers.HyperlinkedRelatedField(read_only=True,lookup_field='public_id',view_name='classes:class-detail',many=True)
    athletes=serializers.HyperlinkedRelatedField(view_name='athletes:athlete-detail',lookup_field='public_id',many=True,read_only=True)
    sport_histories=serializers.HyperlinkedRelatedField(view_name='sporthistories:sporthistory-detail',lookup_field='public_id'
                                                        ,read_only=True,many=True)
    nutrition_plans=serializers.HyperlinkedRelatedField(view_name='plans:nutritionplan-detail',lookup_field='public_id'
                                                       ,many=True,read_only=True)
    class Meta(MidUserSerializer.Meta):
        model = Coach
        fields=MidUserSerializer.Meta.fields+['classes','athletes','sport_histories','nutrition_plans']
    
       