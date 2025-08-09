from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Manager
from .serializers import ManagerSerializer
from .permissions import IsSuperOrManager
# Create your views here.

class ManagerViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Manager.objects.all()

    serializer_class=ManagerSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrManager]
    