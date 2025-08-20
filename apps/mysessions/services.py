from .models import Mysession
from rest_framework.exceptions import ValidationError
class MySessionService:
    
    @classmethod
    def create(cls,serializer):

        days=serializer.validated_data['days']
        start_time=serializer.validated_data['start_time']
        end_time=serializer.validated_data['end_time']
        if Mysession.objects.filter(days__overlap=days,start_time__lt=end_time,end_time__gt=start_time).exists():
            raise ValidationError({'confilicts':'you can not make session in this time because confilict make'})
        serializer.instance=Mysession.objects.create(**serializer.validated_data)

    

    @classmethod
    def update(cls,serializer,instance):
        days=serializer.validated_data.get('days',None)
        start_time=serializer.validated_data.get('start_time',None)
        end_time=serializer.validated_data.get('end_time',None)
        if instance.classes.filter(status='a').exists():
            if days :
                for day in days:
                    extera_days=[]
                    if day  not in instance.days:
                        extera_days.append(day)
                    if extera_days and instance.classes.filter(status='a',days__overlap=extera_days).exists() :
                        raise ValidationError({'days':'unupdate session have active class that not support in this session.you can update this'})
            if start_time:
                if instance.classes.filter(status='a',start_time__lt=start_time).exists():
                    raise ValidationError({'start time':'unupdate session have active class that not support in this session.you can update this'})
            if end_time:
                if instance.classes.filter(status='a',end_time__gt=end_time):
                    raise ValidationError({'end time':'unupdate session have active class that not support in this session.you can update this'})



            for attr,value in serializer.validated_data:
                setattr(instance,attr,value)
            instance.save()

            serializer.instance=instance
                



        else :
            if Mysession.objects.exclude(public_id=instance.public_id).filter(days__overlap=days,start_time__lt=end_time,end_time__gt=start_time).exists():
                raise ValidationError({'confilicts':'you can not make session in this time because confilict make'})
        for attr,value in serializer.validated_data.items():
                setattr(instance,attr,value)
        instance.save()

        serializer.instance=instance


    

    @classmethod
    def delete(cls,instance):
        if instance.classes.filter(status='a').exists():
            raise ValidationError({'class active':'this session have a active class so you can delete this session'})
        instance.delete()  
