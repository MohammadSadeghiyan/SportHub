from .models import Coach
from .serializers import CoachSerializer
from rest_framework import permissions,viewsets
from .permissions import IsSuperOrManagerOrCoach
from django.utils import timezone

from rest_framework.exceptions import ValidationError
class CoachViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user=self.request.user
        if user.is_superuser or user.role=='manager':
            return Coach.objects.all()
        return Coach.objects.get(pk=user.pk)
    lookup_field='public_id'
    lookup_url_kwarg='public_id'
    serializer_class=CoachSerializer
    permission_classes=[permissions.IsAuthenticated,IsSuperOrManagerOrCoach]

    def perform_destroy(self, instance):
        data={}
        if instance.classes.filter(start_date__lte=timezone.now().date,end_date__gte=timezone.now().date).exists():
            data['class']='you have a active class so you cant delete your account and go'
        if instance.balance_rial>0:
            data['balance']='you have a positive balance please first get it and then if dont have a active class, delete'
        if instance.sport_histories.filter(end_date__gte=timezone.now().date,confirmation_coach=True).exsits():
            data['sport history']='you have a active sport history with athlete, so you cant delete your account until that finished'
        if data:raise ValidationError(data)
        else :return instance.delete()

        