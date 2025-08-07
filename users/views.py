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
    
   
    