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
    public_id=ShortUUIDField(editable=False,unique=True)
    name=models.CharField(max_length=100)
    session=models.ManyToManyField(Mysession,related_name='classes')
    start_date=models.DateField()
    days = ArrayField(
        models.CharField(max_length=3, choices=DAYS_OF_WEEK),
        default=list,
        blank=True
    )

    start_time=models.TimeField()
    end_time=models.TimeField()
    end_date=models.DateField()
    capacity=models.PositiveSmallIntegerField()
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='classes')
    class_salary_get_per_athlete_rial=models.DecimalField(max_digits=9,decimal_places=0,validators=[MinValueValidator(0)])
    pricing=models.ForeignKey(ClassItemPricing,on_delete=models.SET_NULL,null=True,related_name='classses')
    
    def __str__(self):
        return f'{self.name}_{self.capacity}'
