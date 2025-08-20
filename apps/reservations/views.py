from rest_framework import viewsets,permissions
from .models import Reservation
from .serializers import ReservationSerializer
from .permissions import ManagerOrAthleteOrReceptionist
from .filters import ReservationFilter
from .helpers import reservation_only_fields
from apps.classes.models import Class
from rest_framework.exceptions import ValidationError
from apps.athletes.models import Athlete
from apps.basicusers.models import BaseUser


class ReservationViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return Reservation.objects.all().select_related('class_ref','reserved_by','athlete')\
                    .only(*reservation_only_fields())
        return Reservation.objects.filter(athlete__public_id=user.public_id).only(*reservation_only_fields())
    
    serializer_class=ReservationSerializer
    lookup_field='public_id'
    permission_classes=[permissions.IsAuthenticated,ManagerOrAthleteOrReceptionist]
    filterset_class=ReservationFilter

    def perform_create(self, serializer):
        if Class.objects.filter(public_id=serializer.validated_data['class_ref'],status='f').exists():
            raise ValidationError({'end_date':'class that you want reserve it is finished'})
        if self.request.user.role in ['manager','receptionist']:
            athlete=serializer.validated_data.pop('athlete')
        else :
            athlete=Athlete.objects.get(public_id=self.request.user.public_id)
        reserved_by=BaseUser.objects.get(public_id=self.request.user.public_id)
        salary_rial=Class.objects.get(public_id=serializer.validated_data['class_ref'].public_id).class_salary_get_per_athlete_rial
        serializer.instance=Reservation.objects.create(athlete=athlete,**serializer.validated_data,salary_rial=salary_rial,reserved_by=reserved_by)

  
    

    def perform_destroy(self, instance):
        if instance.status in ['wait','nack']:
            instance.delete()
        else :
            if instance.class_ref.status=='ia':
                instance.class_ref.coach.balance_rial-=instance.salary_rial
                instance.athlete.balance_rial+=instance.salary_rial
                instance.class_ref.coach.save()
                instance.athlete.save()
                instance.delete()
            else :raise ValidationError({'class start':'you can not delete this reserve because class is start'})