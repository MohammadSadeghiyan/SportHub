from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Order)
admin.site.register(MembershipItem)
admin.site.register(NutritionPlanItem)
admin.site.register(SportHistoryItem)
admin.site.register(ReservationItem)
