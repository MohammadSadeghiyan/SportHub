from django.db import models
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
from django.core.validators import MinValueValidator
from shortuuidfield import ShortUUIDField

class NutritionPlan(models.Model):
    STATUS_CHOICES=(
        ('r','registered'),
        ('nr','not registered'),
        ('f','finished')
    )
    public_id=ShortUUIDField(editable=False,unique=True)
    confirmation_coach=models.BooleanField(default=False)
    athlete=models.ForeignKey(Athlete,on_delete=models.CASCADE,related_name='nutritionplans')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='nutrition_plans')
    name=models.CharField(max_length=40)
    description = models.TextField(blank=True)  
    status=models.CharField(max_length=2,choices=STATUS_CHOICES,default='nr')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    registered_at = models.DateTimeField(null=True)
    salary_rial=models.DecimalField(max_digits=9,decimal_places=0,validators=[MinValueValidator(0)])


    def __str__(self):
        return f'{self.start_date}_{self.end_date}{self.coach}_{self.athlete}'


class Meal(models.Model):
    DAY_CHOICES = [
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
        ('monday','Monday'),
        ('tuesday','Tuesday'),
        ('wednesday','wednesday'),
        ('thursday','Thursday'),
        ('firday','Friday')
    ]
    MEAL_TYPE = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner')
    ]
    public_id=ShortUUIDField(editable=False,unique=True)
    nutrition_plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE, null=True,related_name='meals')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE)
    meal_discription = models.TextField() 
    athlete_date_done=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_day_display()} - {self.get_meal_type_display()}'
