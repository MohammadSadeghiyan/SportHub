from django.db import models
from apps.athletes.models import Athlete
from apps.coaches.models import Coach
from django.db.models import UniqueConstraint
from apps.sporthistories.models import SportHistory
# Create your models here.

class Excersice(models.Model):
    STATUS_TYPE=[
        ('ns','not start'),
        ('w','working'),
        ('f','finished')
    ]
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
        return f'{self.athlete}_{self.name}'

class Excersice_history(models.Model):
    excersice=models.ForeignKey(Excersice,on_delete=models.SET_NULL,null=True,related_name='excersice_history')
    time=models.DateField()
    excersice_time=models.DurationField()
    description=models.TextField()



    def __str__(self):
        return f'{self.excersice.name}_{self.excersice.sport_history.athlete.username}_{self.time}'


    
class NutritionPlan(models.Model):
    athlete=models.ForeignKey(Athlete,on_delete=models.CASCADE,related_name='nutritionplans')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='nutrition_plans')
    name=models.CharField(max_length=40)
    description = models.TextField(blank=True)  
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    registered_at = models.DateTimeField(null=True)
    salary_rial=models.DecimalField(max_digits=9,decimal_places=0)



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

    nutrition_plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE, null=True,related_name='meals')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE)
    meal_discription = models.TextField() 
    athlete_done=models.BooleanField(default=False)
    athlete_date_done=models.DateField(null=True,blank=True)
    athlete_discription=models.TextField() 

    def __str__(self):
        return f'{self.get_day_display()} - {self.get_meal_type_display()}'
