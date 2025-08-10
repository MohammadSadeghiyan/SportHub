from rest_framework import viewsets,permissions
from .models import *
from .serializers import *
from .permissions import *
from .services import *
from drf_spectacular.utils import extend_schema, OpenApiParameter
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
        if user.role=='coach':
            if include:
                return Excersice.objects.filter(sport_history__coach__pk=user.pk).\
                        select_related('sport_history__coach','sport_history__athlete')\
                            .prefetch_related('excersice_history')
            return Excersice.objects.filter(sport_history__coach__pk=user.pk).\
                        select_related('sport_history__athlete','sport_history__coach')
        elif user.role=='athlete':
            if include:
                return Excersice.objects.filter(sport_history__athlete=user.pk)\
                        .select_related('sport_history__athlete')\
                            .prefetch_related('excersice_history')
            return Excersice.objects.filter(sport_history__athlete=user.pk)\
                        .select_related('sport_history__athlete')\
                            .prefetch_related('excersice_history')
                        
    
    lookup_field='public_id'
    serializer_class=ExcersiceSerializer
    permission_classes=[permissions.IsAuthenticated,IsCoachOrAthlete]

    def perform_create(self, serializer):
        sport_history=serializer.validated_data.pop('sport_history')
        excersice_service=ExcersiceService(serializer.validated_data,sport_history=sport_history)
        excersice=excersice_service.create_excersice()
        serializer.instance=excersice
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    
class ExcersiceHistoryViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role=='athlete':
            return Excersice_history.objects.filter(excersice__athlete=user).select_related('excersice__sport_history__athlete')
        elif user.role=='coach':
            return Excersice_history.objects.filter(excersice__coach=user)

    lookup_field='public_id'
    serializer_class=ExcersiceHistorySerializer
    permission_classes=[permissions.IsAuthenticated]