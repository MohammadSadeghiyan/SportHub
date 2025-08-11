from rest_framework import viewsets,permissions
from .models import *
from .serializers import *
from .permissions import *
from .filters import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Prefetch
from rest_framework.exceptions import PermissionDenied
# Create your views here.

@extend_schema(
    parameters=[
        OpenApiParameter(name='include', description='Include related fields', required=False, type=str,enum=['history'])
    ]
)
class ExcersiceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        params = self.request.query_params
        include=params.get('include')      
        excersice_fields=[f.name for f in Excersice._meta.get_fields()]
        history_fields = ['excersice_history__'+f.name for f in Excersice_history._meta.get_fields()] \
                            if include and 'history' in include else ['excersice_history__public_id']
        realted_fields=['sport_history__coach__public_id','sport_history__athlete__public_id'
                        ,'excersice_history__excersice__public_id']
        fields_pass_to_only=excersice_fields+history_fields+realted_fields
        if user.role=='coach':
            return Excersice.objects.filter(sport_history__coach__public_id=user.public_id).\
                    select_related('sport_history__athlete','sport_history__coach')\
                        .prefetch_related(Prefetch('excersice_history',
                                                    queryset=Excersice_history.objects\
                                                        .filter(excersice__sport_history__coach__public_id=user.public_id)\
                                                            .select_related('excersice').only(*history_fields
                                                                                            ,'excersice_history__excersice__public_id')))\
                                            .only(*fields_pass_to_only)
           
        elif user.role=='athlete':
            return Excersice.objects.filter(sport_history__athlete=user.pk)\
                        .select_related('sport_history__athlete')\
                            .prefetch_related(Prefetch('excersice_history',
                                                       queryset=Excersice_history.objects\
                                                        .filter(excersice__sport_history__athlete__public_id=user.public_id)\
                                                            .select_related('excersice').only(*history_fields,
                                                                                            'excersice_history__excersice__public_id')))\
                                            .only(*fields_pass_to_only)
                        
    
    lookup_field='public_id'
    serializer_class=ExcersiceSerializer
    filterset_class=ExcersiceFilter
    permission_classes=[permissions.IsAuthenticated,IsCoachOrAthleteExcersice]


    
    
class ExcersiceHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        excersice_history_fields=[f.name for f in Excersice_history._meta.get_fields()]
        excersice_fields=['excersice__name','excersice__status']
        athlete_fields=['excersice__sport_history__athlete__username']+\
                            ['excersice__sport_history__athlete__public_id' if user.role=='athlete'else None]
        fields_pass_to_only=excersice_history_fields+excersice_fields+athlete_fields
        if user.role=='athlete':
            return Excersice_history.objects.filter(excersice__athlete__public_id=user.public_id)\
                                                .select_related('excersice__sport_history__athlete')\
                                                    .only(*fields_pass_to_only)
        elif user.role=='coach':
            return Excersice_history.objects.filter(excersice__coach__public_id=user.public_id).\
                                                select_related('excersice__sport_history__athlete')\
                                                    .only(*fields_pass_to_only)

    lookup_field='public_id'
    serializer_class=ExcersiceHistorySerializer
    permission_classes=[permissions.IsAuthenticated,IsCoachOrAthleteHistory]
    filterset_class=ExcersiceHistoryFilter
    
    def perform_update(self, serializer):
        excersice=serializer.validated_data.get('excersice')
        if excersice.status!='f':
            return super().perform_update(serializer)
        raise PermissionDenied({'excersice status':'you cant update this excersice history because excersice is finished'})
    
    def perform_destroy(self, instance):
        if instance.excersice.status!='f':
            return super().perform_destroy(instance)
        raise PermissionDenied({'excersice status':'you cant update this excersice history because excersice is finished'})
