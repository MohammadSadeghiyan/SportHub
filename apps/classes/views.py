from rest_framework import viewsets,permissions
from .models import Class
from .serializers import ClassSerializer
from .permissions import ManagerOrRecptionistOrCoachOrAthleteReadOnly
from .filters import *
from django.db.models import Prefetch
from apps.reservations.models import Reservation
from .helpers import class_only_fields
from .services import ClassService


class ClassViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
    
        return Class.objects.all().prefetch_related(Prefetch('reserves',queryset=Reservation.objects.all().only('public_id')))\
                    .select_related('coach')\
                        .prefetch_related(Prefetch('session',queryset=Mysession.objects.all().only('public_id')))\
                            .only(*class_only_fields())
    

    serializer_class=ClassSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrRecptionistOrCoachOrAthleteReadOnly]
    filterset_class=ClassFilter
    lookup_field='public_id'

    def perform_create(self, serializer):
        ClassService.create(self.request,serializer)
    
    def perform_update(self, serializer):
        instance=self.get_object()
        ClassService.update(self.request,instance,serializer) 


    def perform_destroy(self, instance):
        ClassService.delete(instance)
            