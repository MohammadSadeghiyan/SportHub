from apps.athletes.models import Athlete    
from .models import Membership
from .helpers import set_end_date
from rest_framework.exceptions import ValidationError,PermissionDenied
from django.utils import timezone
from apps.coaches.models import Coach
class MembershipService:
    @classmethod
    def create(cls,user,serializer):
        if user.role in ['manager','receptionist']:
            user=serializer.validated_data.pop('user')
        else : 
            if user.role=='athlete':
                user=Athlete.objects.get(public_id=user.public_id)
            else : user=Coach.objects.get(public_id=user.public_id)
        start_date=serializer.validated_data['start_date']
        end_date=set_end_date(start_date,serializer.validated_data.get('type_name'))
        if Membership.objects.filter(user=user,status=True,end_date__gte=start_date).exists():
            raise ValidationError({'exist':'you have a active membership'})
        serializer.instance=Membership.objects.create(user=user,**serializer.validated_data,status=False,end_date=end_date)


    @classmethod
    def update(cls,user,instance,serializer):
        if instance.status==True :
            if instance.start_date>timezone.now().date():
                instance.athlete+=instance.membership_cost_rial
                if user.role in ['manager','receptionist']:
                    user=serializer.validated_data.pop('user',instance.user)
                else : 
                    if user.role=='athlete':
                        user=Athlete.objects.get(public_id=user.public_id)
                    else : user=Coach.objects.get(public_id=user.public_id)
                type_name=serializer.validated_data.get('type_name',instance.type_name)
                start_date=serializer.validated_data.get('start_date',instance.start_date)
                end_date=set_end_date(start_date,type_name)
                membership=Membership.objects.create(user=user,end_date=end_date,start_date=start_date,type_name=type_name)
                instance.delete()
                instance.serializer=membership
            else:
                raise ValidationError({'start':'your membership is start so you can not delete it'})
            

    @classmethod
    def delete(cls,instance):
        if instance.status==True:
            raise PermissionDenied({'status':'you can not delete this membership'})
        instance.delete()


