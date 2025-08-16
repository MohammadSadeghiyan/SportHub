from django.utils import timezone
from .models import SportHistory
from rest_framework.exceptions import ValidationError
from apps.athletes.models import Athlete
class SportHistoryService:
    @classmethod
    def update(cls,instance,serializer):
        if instance.end_date>timezone.now().date():    
            coach=instance.coach
            athlete=instance.athlete
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
            serializer.instance=SportHistory.objects.create(**serializer.validated_data,athlete=new_athlete)

        else : raise ValidationError({'finished':'your history is finished so you can update that'})

    
    @classmethod
    def delete(cls,instance):
        if instance.status=='s':
 
            if instance.start_date>timezone.now().date():    
                coach=instance.coach
                athlete=instance.athlete
                salary=instance.balance_for_coaching_rial
                athlete.balance_rial+=salary
                athlete.save()
                coach.balance_rial-=salary
                coach.save()   

                instance.delete()
        
            else:
                if instance.end_date>timezone.now().date():
                    time_delta = (instance.end_date - timezone.now().date()).days
                    total_days = (instance.end_date - instance.start_date).days 
                    salary = instance.balance_for_coaching_rial * (time_delta / total_days)
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
        
        serializer.instance=SportHistory.objects.create(**serializer.validated_data,athlete=athlete,status='ns')



        