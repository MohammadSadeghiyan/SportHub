from rest_framework import viewsets,permissions
from .models import *
from .serializers import *
from .permissions import *
from .filters import *
from .helpers import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Prefetch
from drf_spectacular.types import OpenApiTypes
from rest_framework.exceptions import PermissionDenied
# Create your views here.

@extend_schema(
    parameters=[
        OpenApiParameter(name='include', description='Include related fields',location=OpenApiParameter.QUERY,
                                                 required=False, type=str,enum=['history']),
        OpenApiParameter(name='end_date', description='date of ending report time(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='end_date__gte', description='date of ending excersice time is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='end_date__lte', description='date of ending excersice time is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),

        OpenApiParameter(name='start_date', description='date of start excersice (djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
            
        OpenApiParameter(name='start_date__gte', description='date of start excersice is grater than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        
        OpenApiParameter(name='start_date__lte', description='date of start excersice is less than or equal(djalali date(shamsi))'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.DATE),
        OpenApiParameter(name='sport_history', description='uuid of sport history related to the excersice'
                         ,location=OpenApiParameter.QUERY, required=False, type=OpenApiTypes.UUID)
    ]
)
class ExcersiceViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        params = self.request.query_params
        fields_pass_to_only,history_fields=get_fields_excersice_pass_to_only(params)
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


    

@extend_schema( 
    parameters=[
        OpenApiParameter(name='excersice', description='public_id of excersice iexact',location=OpenApiParameter.QUERY, 
                         required=False, type=OpenApiTypes.UUID),
       
         OpenApiParameter(name='description_icontains', description='description of report excersice history contain'
                          ,location=OpenApiParameter.QUERY,required=False, type=str), 
        ]   )
class ExcersiceHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        fields_pass_to_only=get_fields_excersice_history_pass_to_only(user)
        if user.role=='athlete':
            return Excersice_history.objects.filter(excersice__sport_history__athlete__public_id=user.public_id)\
                                                .select_related('excersice__sport_history__athlete')\
                                                    .only(*fields_pass_to_only)
        elif user.role=='coach':
            return Excersice_history.objects.filter(excersice__coach__public_id=user.public_id).\
                                                select_related('excersice__sport_history__athlete','excersice__sport_history__coach')\
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
