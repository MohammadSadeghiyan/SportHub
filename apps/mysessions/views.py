from rest_framework import viewsets,permissions
from .models import Mysession
from .serializers import MySessionSerializer
from .filters import MySessionFilter
from .permissions import ManagerOrRecptionistOrCoachReadOnlyOrAthleteReadOnly
from django.db.models import Prefetch
from apps.classes.models import Class
from .services import MySessionService


class MySessionViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return Mysession.objects.all().prefetch_related(Prefetch('classes',queryset=Class.objects.all().only('public_id')))
    
    serializer_class=MySessionSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrRecptionistOrCoachReadOnlyOrAthleteReadOnly]
    lookup_field='public_id'
    filterset_class=MySessionFilter

    def perform_create(self, serializer):
       MySessionService.create(serializer)
    
    def perform_destroy(self, instance):
          MySessionService.delete(instance)

    def perform_update(self, serializer):
        instance=self.get_object()
        MySessionService.update(serializer,instance)