from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.

class Gym(models.Model):
    input_salary=models.DecimalField(max_digits=18,decimal_places=0,validators=[MinValueValidator(0)])
    ouput_salary=models.DecimalField(max_digits=18,decimal_places=0,validators=[MinValueValidator(0)])
