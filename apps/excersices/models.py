from django.db import models
from django.db.models import UniqueConstraint
from apps.sporthistories.models import SportHistory
from shortuuidfield import ShortUUIDField
# Create your models here.



class Excersice(models.Model):
    STATUS_TYPE=[
        ('ns','not start'),
        ('w','working'),
        ('f','finished')
    ]
    public_id=ShortUUIDField(unique=True,editable=False)
    name=models.CharField()
    sport_history=models.ForeignKey(SportHistory,on_delete=models.CASCADE,related_name='excersices')
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField(blank=True,null=True)
    status=models.CharField(max_length=2,choices=STATUS_TYPE,default='ns')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['sport_history','name'],
                name='unique_excersice'
            )
        ]

    def __str__(self):
        return f'{self.sport_history.athlete.username}_{self.name}'

class Excersice_history(models.Model):
    public_id=ShortUUIDField(editable=False,unique=True)
    excersice=models.ForeignKey(Excersice,on_delete=models.CASCADE,related_name='excersice_history')
    time=models.DateField()
    excersice_time=models.DurationField()
    description=models.TextField()



    def __str__(self):
        return f'{self.excersice.name}_{self.excersice.sport_history.athlete.username}_{self.time}'

