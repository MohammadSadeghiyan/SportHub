from apps.coaches.models import Coach
from apps.classes.models import Class
from rest_framework.exceptions import ValidationError
from apps.pricing.models import ClassItemPricing
from django.utils import timezone
from .helpers import count_class_days,hours_between
from decimal import Decimal
class ClassService:

    @classmethod
    def create(cls,request,serializer):
        user=request.user
        if user.role=='coach':
            coach=Coach.objects.get(public_id=user.public_id)
        else :coach=serializer.validated_data.pop('coach')
        days=serializer.validated_data['days']
        start_date=serializer.validated_data['start_date']
        end_date=serializer.validated_data['end_date']
        start_time=serializer.validated_data['start_time']
        end_time=serializer.validated_data['end_time']
        session=serializer.validated_data.get('session')
        capacity=serializer.validated_data['capacity']
        conflicts = Class.objects.filter(coach=coach).filter(days__overlap=days)\
                        .filter(start_date__lte=end_date,end_date__gte=start_date)\
                            .filter(start_time__lt=end_time,end_time__gt=start_time)
        if conflicts.exists():
            raise ValidationError({'confilict':'you have already class in this time'})
        pricing=ClassItemPricing.objects.filter(start_start_date__lte=start_date,end_start_date__gte=start_date,session_ref=session,
                                        max_capacity__gte=capacity,min_capacity__lte=capacity)
        if not pricing.exists():
            raise ValidationError({'pricing policy not exist':'policy pricing for this information isnot exits . please talk with receptionists'})
        class_salary_get_per_athlete_rial = Decimal(pricing.first().price_per_hour) * Decimal(hours_between(start_time, end_time)) * count_class_days(start_date, end_date, days)
        if start_date>timezone.now().date():status='ia'
        else:status='ac'
        serializer.instance=Class.objects.create(coach=coach,**serializer.validated_data
                                                 ,class_salary_get_per_athlete_rial=class_salary_get_per_athlete_rial,status=status)
        

    @classmethod
    def update(cls,request,instance,serializer):
         
        user=request.user
        if user.role=='coach':
            coach=Coach.objects.get(public_id=user.public_id)
        else :coach=serializer.validated_data.get('coach',instance.coach)
        days=serializer.validated_data.instance.get('days',instance.days)
        start_date=serializer.validated_data.get('start_date',instance.start_date)
        end_date=serializer.validated_data.get('end_date',instance.end_date)
        start_time=serializer.validated_data.get('start_time',instance.start_time)
        end_time=serializer.validated_data.get('end_time',instance.end_time)
        session=serializer.validated_data.get('session',instance.session)
        capacity=serializer.validated_data.get('capacity',instance.capacity)

        confilicts=Class.objects.exclude(public_id=instance.public_id).filter(coach=coach).filter(days__overlap=days)\
                        .filter(start_date__lte=end_date,end_date__gte=start_date)\
                            .filter(start_time__lt=end_time,end_time__gt=start_time)
        if confilicts.exists():
            raise ValidationError({'confilict':'you have already class in this time'})
        pricing=ClassItemPricing.objects.filter(start_start_date__lte=start_date,end_start_date__gte=start_date,session_ref=session,
                                        max_capacity__gte=capacity,min_capacity__lte=capacity)
        if not pricing.exists():
            raise ValidationError({'pricing policy not exist':'policy pricing for this information isnot exits . please talk with receptionists'})
        class_salary_get_per_athlete_rial = Decimal(pricing.first().price_per_hour) * Decimal(hours_between(start_time, end_time)) * count_class_days(start_date, end_date, days)
        if start_date>timezone.now().date():status='ia'
        else:status='ac'
        athlete_class=instance.reserves.filter(status='ack').value_list('athlete',flat=True)
        if athlete_class:

            for athlete in athlete_class:
                athlete.balance_rial+=instance.class_salary_get_per_athlete_rial
                instance.coach-=instance.class_salary_get_per_athlete_rial
                athlete.save()
            instance.coach.save()

        instance.delete()
        #add celery for message to users of class if want get new class
        serializer.instance=Class.objects.create(coach=coach,**serializer.validated_data
                                                 ,class_salary_get_per_athlete_rial=class_salary_get_per_athlete_rial,status=status)
       


    @classmethod
    def delete(instance):
        if instance.status=='a':
            raise ValidationError({'start class':'class start so you can delete that'})
        
        if instance.status=='c':
            return super().perform_destroy(instance)
        athlete_class=instance.reserves.filter(status='ack').value_list('athlete',flat=True)
        if athlete_class:

            for athlete in athlete_class:
                athlete.balance_rial+=instance.class_salary_get_per_athlete_rial
                instance.coach-=instance.class_salary_get_per_athlete_rial
                athlete.save()

            instance.coach.save()
            return instance.delete()
        
        return instance.delete()
