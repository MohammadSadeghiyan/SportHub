from rest_framework import viewsets,permissions
from .models import *
from .serializers import *
from .permissions import IsManagerOrRecptionist
from rest_framework.decorators import action

class ReceptionistViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user=self.request.user
        if user.role=='manager':
            return Receptionist.objects.all()
        return Receptionist.objects.get(pk=user.pk)
    serializer_class=ReceptionistSerializer
    permission_classes=[permissions.IsAuthenticated,IsManagerOrRecptionist]

    

    