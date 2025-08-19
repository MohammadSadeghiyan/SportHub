from .models import NutritionPlan
from apps.athletes.models import Athlete
from rest_framework.exceptions import ValidationError
class NutritionplanService:

    @classmethod
    def create(cls,user,serializer):
        if user.role in ['manager','receptionist']:
            athlete=serializer.validated_data.pop('athlete')
            coach=serializer.validated_data.pop('coach')
        elif user.role =='athlete':
            athlete=Athlete.objects.get(public_id=user.public_id)
            coach=serializer.validated_data.pop('coach')
        serializer.instance=NutritionPlan.objects.create(coach=coach,athlete=athlete,**serializer.validated_data)


    
    @classmethod
    def update(cls,instance,serializer):
        if instance.status=='s':
            athlete=serializer.validated_data.get('athlete',instance.athlete)
            coach=serializer.validated_data.get('coach',instance.coach)
            if athlete!=instance.athlete or coach!=instance.coach:
                raise ValidationError({'status':'you can not change athlete or coach of nutrition plans that start'})
            else:
                start_date=serializer.validated_data.get('start_date',instance.start_date)
                end_date=serializer.validated_data.get('end_date',instance.end_date)
                if end_date!=instance.end_data and instance.start_date!=start_date:
                    instance.status='ns'
                    instance.confirmation_coach=False
                    instance.coach.balance_rial-=instance.salary_rial
                    instance.athlete.balance_rial+=instance.salary_rial
                    instance.athlete.save()
                    instance.coach.save()

                    for attr,val in serializer.validated_data.items():
                        if attr !='confirmatoin_coach':
                            setattr(instance,attr,val)

                    instance.save()
                
                else :
                    for attr,val in serializer.validated_data.items():
                            setattr(instance,attr,val)

                    instance.save()

        else:
            for attr,val in serializer.validated_data.items():
                    setattr(instance,attr,val)

            instance.save()

        serializer.instance=instance
    

    @classmethod 
    def delete(cls,instance):
        if instance.status=='r':
           raise ValidationError({'registered':'you can not delete this plan because is registered'})
        instance.delete()