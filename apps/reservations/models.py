from django.db import models
from apps.classes.models import Class
from apps.basicusers.models import MidUser
from apps.athletes.models import Athlete
from django.core.validators import MinValueValidator
# Create your models here.

class Reservation(models.Model):
    STATUS_CHOICES=[
        ('ack','accepted'),
        ('nack','not accepted'),
        ('wait','waiting_list')
    ]
    class_ref=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True,related_name='reserves')
    athlete=models.ForeignKey(Athlete,on_delete=models.SET_NULL,null=True,related_name='reserves')
    salary_rial=models.DecimalField(max_digits=9,decimal_places=0,validators=[MinValueValidator(0)])
    status=models.CharField(max_length=4,choices=STATUS_CHOICES,default='wait')
    date=models.DateTimeField(auto_now_add=True)
    reserved_by=models.ForeignKey(MidUser,on_delete=models.SET_NULL,null=True,related_name='reserve_requests')
    registered_date=models.DateField(null=True)

    def __str__(self):
        return f'{self.class_ref.name}_{self.status}'