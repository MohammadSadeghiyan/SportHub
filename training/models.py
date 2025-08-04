from django.db import models
from users.models import Coach,Athlete
# Create your models here.

class Session(models.Model):
    DAY_CHOICES=[
        ('even','Even'),
        ('odd','Odd'),
        ('all','All')
    ]
    days_of_week=models.CharField(max_length=4,choices=DAY_CHOICES)
    start_time=models.TimeField()
    end_time=models.TimeField()

    def __str__(self):
        return f'{self.pk}_{self.days_of_week}'



class Class(models.Model):
    name=models.CharField(max_length=100)
    session=models.ForeignKey(Session,on_delete=models.SET_NULL,null=True,related_name='classes')
    start_date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    end_date=models.DateField()
    capacity=models.PositiveSmallIntegerField()
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='classes')
    salary_to_gym_per_athlete_rail=models.DecimalField(max_digits=15,decimal_places=0,blank=True,null=True)
    class_salary_get_per_athlete_rial=models.DecimalField(max_digits=15,decimal_places=0)

    @property
    def get_full_price(self):
        if self.pk:
            athlete_registered=self.reserves.filter(status='ack')
            total=0
            for athlete in athlete_registered:
                total+=athlete.salary_rial-self.salary_to_gym_per_athlete_rail
            return total
        
    
    def __str__(self):
        return f'{self.name}_{self.capacity}'

class Reservation(models.Model):
    STATUS_CHOICES=[
        ('ack','accepted'),
        ('nack','not accepted'),
        ('wait','waiting_list')
    ]
    class_ref=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True,related_name='reserves')
    athlete=models.ForeignKey(Athlete,on_delete=models.SET_NULL,null=True,related_name='reserves')
    salary_rial=models.DecimalField(max_digits=15,decimal_places=0)
    status=models.CharField(max_length=4,choices=STATUS_CHOICES,default='wait')
    

    def __str__(self):
        return f'{self.class_ref.name}_{self.status}'