from rest_framework import serializers
from .models import SportHistory
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from apps.djalalidates.serializers import JalaliDateField
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
from typing import Union
from .helpers import *
from apps.djalalidates.helpers import start_date_validator


class SportHistorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='sport-histories:sport-history-detail',
        read_only=True,
        lookup_field='public_id'  
    )
    coach = serializers.SlugRelatedField(queryset=Coach.objects.all(), slug_field='public_id')
    athlete = serializers.SlugRelatedField(queryset=Athlete.objects.all(), slug_field='public_id')
    excersices = serializers.SerializerMethodField()
    start_date = JalaliDateField()
    end_date = JalaliDateField()

    class Meta:
        model = SportHistory
        fields = [
            'url','public_id','coach','athlete','start_date','end_date','confirmation_coach','balance_for_coaching_rial','status',
            'excersices',
        ]
        read_only_fields = ('balance_for_coaching_rial', 'status')

    def validate_start_date(self, value):
        start_date_validator(value)
        return value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('request').user
        if user.role == 'coach':
            read_only_fields = coach_sport_history_serializer_read_only_fields()
            for field in read_only_fields:
                self.fields[field].read_only = True

        elif user.role == 'athlete':
            read_only_fields = athlete_sport_history_serializer_read_only_fields()
            for field in read_only_fields:
                self.fields[field].read_only = True
        else:
            self.fields['confirmation_coach'].read_only = True

    @extend_schema_field(Union[OpenApiTypes.URI, None])
    def get_excersices(self, obj):
        request = self.context.get('request')
        include = request.query_params.get('include', '')
        if 'excersice' in include:
            return make_uri_excersice(obj, request)
        return None
