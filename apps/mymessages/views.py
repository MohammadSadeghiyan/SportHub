from .models import *
from .permissions import *
from .filters import *
from .serializers import *
from rest_framework import viewsets,permissions
from django.db.models import Q
from apps.basicusers.models import MidUser

class MyMessageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role=='manager':
            return Mymessage.objects.all().select_related('sender','reciver')\
                .only('text','titel','sender__public_id','reciver__public_id','created_at','updated_at','public_id','id')
        return Mymessage.objects.filter(Q(sender__public_id=user.public_id)|Q(reciver__public_id=user.public_id))\
                    .select_related('sender','reciver')\
                        .only('text','titel','sender__public_id','reciver__public_id','created_at','updated_at','public_id','id')
    
    serializer_class=MyMessageSerializer
    permission_classes=[permissions.IsAuthenticated,SenderOrReciverOrManager]
    lookup_field='public_id'
    filterset_class=MessageFilter

    def perform_create(self, serializer):
        sender=MidUser.objects.get(public_id=self.request.user.public_id)
        serializer.instance=Mymessage.objects.create(**serializer.validated_data,sender=sender)
    



    
