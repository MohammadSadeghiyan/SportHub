from django.contrib import admin
from .models import NutritionPlan
from .models import Meal
# Register your models here.
admin.site.register(NutritionPlan)
admin.site.register(Meal)