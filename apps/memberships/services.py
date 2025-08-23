from .models import Membership
from .helpers import set_end_date
from rest_framework.exceptions import ValidationError,PermissionDenied
from apps.basicusers.models import MidUser
from apps.pricing.models import MembershipPricing
from apps.orders.models import Order,MembershipItem

class MembershipService:
    @classmethod
    def create(cls,user,serializer):
        if user.role in ['manager','receptionist']:
            user=serializer.validated_data.pop('user')
        else : 
            user=MidUser.objects.get(public_id=user.public_id)
        start_date=serializer.validated_data.get('start_date')
        end_date=set_end_date(start_date,serializer.validated_data.get('type_name'))
        
        if Membership.objects.filter(user=user,status_activation=True,end_date__gte=start_date).exists():
            raise ValidationError({'exist':'you have a request membership'})
        
        qs=MembershipPricing.objects.filter(start_start_date__lte=start_date,end_start_date__gte=start_date)
        if qs.exists():
            pricing=qs.first()
            membership_cost_rial=pricing.price
            serializer.instance=Membership.objects.create(user=user,**serializer.validated_data,status='ns',end_date=end_date,
                                                          membership_cost_rial=membership_cost_rial)
           
            
        else :
            raise ValidationError({'pricing not exist':'pricing for this membership type and date not exist please talk to the receptionist'})


    @classmethod
    def update(cls,user,instance,serializer):
        if instance.status_activation==True :
            raise ValidationError({'start':'your membership is start so you can not delete it'})

        else :
                if user.role in ['manager','receptionist']:
                    user=serializer.validated_data.pop('user',instance.user)
                else : 
                    user=MidUser.objects.get(public_id=user.public_id)
                
                type_name=serializer.validated_data.get('type_name',instance.type_name)
                start_date=serializer.validated_data.get('start_date',instance.start_date)
                end_date=set_end_date(start_date,type_name)
                instance.end_date=end_date
                instance.type_name=type_name
                instance.start_date=start_date
                instance.user=user
                
                pended_order=Order.objects.filter(user=user,status='pending')
                pended_order=pended_order.first()
                pended_order.price-=instance.membership_cost_rial
                pended_order.save()

                qs=MembershipPricing.objects.filter(start_start_date__lte=start_date,end_start_date__gte=start_date)
                if qs.exists():
                    pricing=qs.first()
                    instance.membership_cost_rial=pricing.price
                    instance.save()
                    serializer.instance=instance

                    
                
                else :
                    raise ValidationError({'pricing not exist':'pricing for this membership type and date not exist please talk to the receptionist'})
            
            
                
                
                
            
            

    @classmethod
    def delete(cls,instance):
        if instance.status==True:
            raise PermissionDenied({'status':'you can not delete this membership'})


        instance.delete()


