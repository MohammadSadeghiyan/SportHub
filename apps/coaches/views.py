from .models import Coach
from .serializers import *
from rest_framework import permissions,viewsets
from .permissions import IsManagerOrCoachOrReadOnly
from .filters import CoachFilter
from django.db.models import Prefetch
from apps.athletes.models import Athlete
from .services import *
class CoachViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role!='coach':
            return Coach.objects.all().prefetch_related('classes')
        return Coach.objects.filter(public_id=user.public_id).prefetch_related('classes','sport_histories',
                                                                               Prefetch('athletes'
                                                                                        ,queryset=Athlete.objects.all()\
                                                                                            .only('public_id')))
    
    def get_serializer_class(self):
        if self.request.user.role=='athlete':
            return PublicCoachSerializer
        return CoachSerializer

    lookup_field='public_id'
    permission_classes=[permissions.IsAuthenticated,IsManagerOrCoachOrReadOnly]
    filterset_class=CoachFilter

    def perform_destroy(self, instance):
        delete_coach(instance)
     
        