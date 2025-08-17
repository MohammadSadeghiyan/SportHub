from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
def delete_athlete(instance):
        data={}
        if instance.reserves.filter(status='ack').exists() and instance.reserves.class_ref.filter(start_date__lte=timezone.now().date()
                                                                                  ,end_date__gte=timezone.now().date()).exists():
            data['class']='you have a active class so you cant delete your account and go'
        if instance.balance_rial:
            data['balance']='you have a positive balance please first get it and then if dont have a active class, delete'
        if instance.sport_histories.filter(start_date__lte=timezone.now().date(),end_date__gte=timezone.now().date(),status='s').exists():
            data['sport history']='you have a active sport history with athlete, so you cant delete your account until that finished'
        if data:raise PermissionDenied(data)
        else :return instance.delete()