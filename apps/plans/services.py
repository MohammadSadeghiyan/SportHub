from .models import NutritionPlan
from apps.athletes.models import Athlete
from rest_framework.exceptions import ValidationError
from apps.pricing.models import NutritionPricing
from decimal import Decimal
from apps.orders.models import Order
class NutritionplanService:

    @classmethod
    def create(cls,user,serializer):
        if user.role in ['manager','receptionist']:
            athlete=serializer.validated_data.pop('athlete')
            coach=serializer.validated_data.pop('coach')
        elif user.role =='athlete':
            athlete=Athlete.objects.get(public_id=user.public_id)
            coach=serializer.validated_data.pop('coach')
        start_date=serializer.validated_data.get('start_date')
        end_date=serializer.validated_data.get('end_date')
        pricing=NutritionPricing.objects.filter(start_start_date__lt=start_date,end_start_date__gt=start_date)
        if pricing.exists():
            salary=pricing.first().price_per_day*Decimal((end_date-start_date).days)
            serializer.instance=NutritionPlan.objects.create(coach=coach,athlete=athlete,**serializer.validated_data,salary_rial=salary)
        else:
            raise ValidationError({'pricing policy not exist':'please tell to the manager or receptionist'})


    
    @classmethod
    def update(cls, instance, serializer):
        data = serializer.validated_data
        start_date = data.get('start_date', instance.start_date)
        end_date = data.get('end_date', instance.end_date)
        athlete = data.get('athlete', instance.athlete)
        coach = data.get('coach', instance.coach)

        if instance.status == 'r':
            if athlete != instance.athlete or coach != instance.coach:
                raise ValidationError({
                    'status': 'You cannot change athlete or coach of started nutrition plans'
                })

            if start_date != instance.start_date or end_date != instance.end_date:
                instance.status = 'nr'
                instance.confirmation_coach = False
                instance.coach.balance_rial -= instance.salary_rial
                instance.athlete.balance_rial += instance.salary_rial
                instance.athlete.save()
                instance.coach.save()
        else:
                pended_order=Order.objects.filter(user=athlete,status='pending')
                pended_order=pended_order.first()
                pended_order.price-=instance.salary_rial
                pended_order.save()
        for attr, val in data.items():
            if attr != 'confirmation_coach':
                setattr(instance, attr, val)

        pricing = NutritionPricing.objects.filter(
            start_start_date__lt=start_date,
            end_start_date__gt=start_date
        ).first()

        if not pricing:
            raise ValidationError({
                'pricing_policy_not_exist': 'Please tell to the manager or receptionist'
            })
        
        instance.confirmation_coach=False
        instance.salary_rial = pricing.price_per_day * Decimal((end_date - start_date).days)
        instance.save()

        serializer.instance = instance


    @classmethod 
    def delete(cls,instance):
        if instance.status=='r':
           raise ValidationError({'registered':'you can not delete this plan because is registered'})
        instance.delete()



class MealService:

    @classmethod
    def create(cls,serializer):
        plan=serializer.validated_data['nutrition_plan']
        if plan.status!='r':
            raise ValidationError({'plan finished or not registered':'you can not create meal that relative to the plans that finished'})
        serializer.save()

    @classmethod 
    def delete(cls,instance):
        if instance.nutrition_plan.status=='f':
            raise ValidationError({'plan finished':'you can not meal that relative to the plans that finished'})
        instance.delete()

    
    @classmethod
    def update(cls,serializer,instance):
        if instance.nutrition_plan.status=='f':
            raise ValidationError({'plan finished':'you can not update meal that relative to the plans that finished'})
        for attr,val in serializer.validated_data.items():
            setattr(instance,attr,val)

        instance.save()
        serializer.instance=instance