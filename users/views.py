from rest_framework import viewsets,permissions
from .models import *
from .serializers import *
from .permissions import *

# Create your views here.
class ManagerViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Manager.objects.all()

    serializer_class=ManagerSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrManager]
    
   

class ReceptionistViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user=self.request.user
        if user.is_superuser or user.role=='manager':
            return Receptionist.objects.all()
        return Receptionist.objects.get(pk=user.pk)
    serializer_class=ReceptionistSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrManagerOrRecption]
