from .models import *
from .permissions import *
from .filters import *
from .serializers import *
from rest_framework import viewsets,permissions
from django.db.models import Q
from django.utils import timezone
from rest_framework.response import Response
from .helpers import message_only_fields

class MyMessageViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptioist']:
            return Mymessage.objects.all().select_related('sender','reciver')\
                .only(*message_only_fields())
        return Mymessage.objects.filter(Q(sender__public_id=user.public_id)|Q(reciver__public_id=user.public_id))\
                    .select_related('sender','reciver')\
                        .only(*message_only_fields())
    
    serializer_class=MyMessageSerializer
    permission_classes=[permissions.IsAuthenticated,SenderOrReciverOrManager]
    lookup_field='public_id'
    filterset_class=MessageFilter

    def retrieve(self, request, *args, **kwargs):
        instance=self.get_object()
        user=request.user
        if instance.reciver==user and instance.read_status=='n':
            instance.read_status='r'
            instance.read_date=timezone.now().date()
            instance.read_time=timezone.now().time()
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        sender=self.request.user
        serializer.instance=Mymessage.objects.create(**serializer.validated_data,sender=sender)
    



    
