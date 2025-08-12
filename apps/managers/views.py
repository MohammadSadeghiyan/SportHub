from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Manager
from .serializers import ManagerSerializer
from .permissions import IsSuperOrManager
from django.db.models import Prefetch
from apps.reports.models import Report
# Create your views here.

class ManagerViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Manager.objects.all().prefetch_related(Prefetch('reports',
                                                      queryset=Report.objects.filter(manager__public_id=self.request.user.public_id)\
                                                        .only('public_id')))
    lookup_field='public_id'
    serializer_class=ManagerSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrManager]
    