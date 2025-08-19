from django.db import models
from apps.coaches.models import Coach
from apps.mysessions.models import Mysession
from django.core.validators import MinValueValidator
from shortuuidfield import ShortUUIDField
from django.contrib.postgres.fields import ArrayField
from apps.pricing.models import ClassItemPricing
# Create your models here.


class Class(models.Model):
    DAYS_OF_WEEK = (
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
)
    STATUS_CHOICES=(
        ('a','Active'),
        ('ia','Inactive'),
        ('f','Finished')
    )
    public_id=ShortUUIDField(editable=False,unique=True)
    name=models.CharField(max_length=100)
    session=models.ManyToManyField(Mysession,related_name='classes')
    start_date=models.DateField()
    days = ArrayField(
        models.CharField(max_length=3, choices=DAYS_OF_WEEK),
        default=list,
        blank=True
    )
    status=models.CharField(max_length=2,choices=STATUS_CHOICES,default='ia')
    start_time=models.TimeField()
    end_time=models.TimeField()
    end_date=models.DateField()
    capacity=models.PositiveSmallIntegerField()
    count_registered=models.PositiveSmallIntegerField(null=True)
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='classes')
    class_salary_get_per_athlete_rial=models.DecimalField(max_digits=9,decimal_places=0,blank=True,validators=[MinValueValidator(0)])
    
    def __str__(self):
        return f'{self.name}_{self.capacity}'
