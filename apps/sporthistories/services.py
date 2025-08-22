from django.utils import timezone
from .models import SportHistory
from rest_framework.exceptions import ValidationError
from apps.athletes.models import Athlete
from apps.orders.models import Order
from decimal import Decimal
from apps.pricing.models import SportHistoryPricing
from django.db.models import Q


class SportHistoryService:
    @classmethod
    def update(cls,instance,serializer):
        coach=instance.coach
        athlete=instance.athlete
        if instance.status=='r':
            if instance.end_date>timezone.now().date():    
                
                instance.status='c'
                instance.save()
            

            if instance.start_date >timezone.now().date():
                salary=instance.balance_for_coaching_rial
            else:
                time_delta = (instance.end_date - timezone.now().date()).days
                total_days = (instance.end_date - instance.start_date).days 
                salary = instance.balance_for_coaching_rial * (time_delta / total_days)

            athlete.balance_rial+=salary
            athlete.save()
            coach.balance_rial-=salary
            coach.save()   

            new_athlete=serializer.validated_data.pop('athlete',instance.athlete)
            start_date=serializer.validated_data.pop('start_date',instance.start_date)
            end_date=serializer.validated_data.pop('end_date',instance.end_date)
            coach=serializer.validated_data.pop('coach',instance.coach)
            overlapping_histories = SportHistory.objects.filter(athlete=athlete,status='r')\
                                .filter(Q(start_date__lte=end_date, end_date__gte=start_date) |
                                    Q(start_date__gte=start_date, start_date__lte=end_date) |
                                         Q(end_date__gte=start_date, end_date__lte=end_date)
            )
        
            if overlapping_histories.exists():
                raise ValidationError({
                'sport_history': 'You have a sport history in this time period and cannot create a new one'
                })
            priceing=SportHistoryPricing.objects.filter(start_start_date__lte=start_date,end_start_date__gte=start_date)
            if priceing.exists():
                balance_for_coaching_rial=priceing.first().price_per_day*((end_date-start_date).days)
                serializer.instance=SportHistory.objects.create(start_date=start_date,athlete=new_athlete,end_date=end_date,coach=coach,
                                                            balance_for_coaching_rial=balance_for_coaching_rial)

            else :raise ValidationError({'sport price':'price for this sport history is not defined please talk with gym receptionists'})
        else:
            pended_order=Order.objects.filter(user=athlete,status='pending')
            pended_order=pended_order.first()
            pended_order.price-=instance.balance_for_coaching_rial
            pended_order.save()   
        
            for attr,val in serializer.validated_data.items():
                setattr(instance,attr,val)
            overlapping_histories = SportHistory.objects.filter(status='r',athlete=instance.athlete)\
                                .filter(Q(start_date__lte=instance.end_date, end_date__gte=instance.start_date) |
                                    Q(start_date__gte=instance.start_date, start_date__lte=instance.end_date) |
                                         Q(end_date__gte=instance.start_date, end_date__lte=instance.end_date)
            )
        
            if overlapping_histories.exists():
                raise ValidationError({
                'sport_history': 'You have a sport history in this time period and cannot create a new one'
                })
            priceing=SportHistoryPricing.objects.filter(start_start_date__lte=instance.start_date,end_start_date__gte=instance.start_date)
            if priceing.exists():
                balance_for_coaching_rial=priceing.first().price_per_day*((instance.end_date-instance.start_date).days)
                print((instance.end_date-instance.start_date).days)
                instance.balance_for_coaching_rial=balance_for_coaching_rial
                instance.save()
                serializer.instance=instance
            else :raise ValidationError({'sport price':'price for this sport history is not defined please talk with gym receptionists'})
           

    
    @classmethod
    def delete(cls,instance):
        if instance.status=='r':
            coach=instance.coach
            athlete=instance.athlete
            salary=instance.balance_for_coaching_rial

            if instance.start_date>timezone.now().date():    
               
                athlete.balance_rial+=salary
                athlete.save()
                coach.balance_rial-=salary
                coach.save()   

                instance.delete()
        
            else:
                if instance.end_date>timezone.now().date():
                    time_delta = (instance.end_date - timezone.now().date()).days
                    total_days = (instance.end_date - instance.start_date).days 
                    salary = instance.balance_for_coaching_rial * Decimal(time_delta / total_days)
                    athlete.balance_rial+=salary
                    athlete.save()
                    coach.balance_rial-=salary
                    coach.save()   

                    instance.delete()
                
                
                else : instance.delete()
        
        else : instance.delete()

    @classmethod
    def create(cls,serializer,user):
        if user.role=='athlete':
            athlete= Athlete.objects.get(public_id=user.public_id)
        else:
            athlete=serializer.validated_data.pop('athlete')
        end_date=serializer.validated_data.get('end_date')
        start_date=serializer.validated_data.get('start_date')
        overlapping_histories = SportHistory.objects.filter(status='r',athlete=athlete).filter(Q(start_date__lte=end_date, end_date__gte=start_date) |
                                    Q(start_date__gte=start_date, start_date__lte=end_date) |
                                         Q(end_date__gte=start_date, end_date__lte=end_date)
        )
        
        if overlapping_histories.exists():
            raise ValidationError({
                'sport_history': 'You have a sport history in this time period and cannot create a new one'
            })
        
        priceing=SportHistoryPricing.objects.filter(start_start_date__lte=start_date,end_start_date__gte=start_date)
        if priceing.exists():
            balance_for_coaching_rial=priceing.first().price_per_day*((end_date-start_date).days)
            serializer.instance=SportHistory.objects.create(**serializer.validated_data,athlete=athlete
                                                            ,balance_for_coaching_rial=balance_for_coaching_rial)

        else :raise ValidationError({'sport price':'price for this sport history is not defined please talk with gym receptionists'})
       


        