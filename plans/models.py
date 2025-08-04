from django.db import models
from users.models import Athlete,Coach
from django.db.models import UniqueConstraint
# Create your models here.

class Excersice(models.Model):
    STATUS_TYPE=[
        ('ns','not start'),
        ('w','working'),
        ('f','finished')
    ]
    name=models.CharField()
    athlete=models.ForeignKey(Athlete,on_delete=models.SET_NULL,null=True,related_name='excersices')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='excersices')
    description=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField(blank=True,null=True)
    status=models.CharField(max_length=2,choices=STATUS_TYPE,default='ns')

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['athlete','name'],
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
        return f'{self.excersice.name}_{self.excersice.athlete}_{self.time}'


    
class NutritionPlan(models.Model):
    athlete=models.ForeignKey(Athlete,on_delete=models.SET_NULL,null=True,related_name='nutritionplans')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='nutritionplan')
    name=models.CharField(max_length=40)
    description = models.TextField(blank=True)  
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    salary_rial=models.DecimalField(max_digits=15,decimal_places=0)



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

    nutrition_plan = models.ForeignKey(NutritionPlan, on_delete=models.CASCADE, related_name='meals')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPE)
    content = models.TextField()  

    def __str__(self):
        return f'{self.get_day_display()} - {self.get_meal_type_display()}'
