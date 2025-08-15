from django.contrib import admin
from .models import ClassPricing,NutritionPricing,MembershipPricing,SportHistoryPricing
# Register your models here.

admin.site.register(ClassPricing)
admin.site.register(MembershipPricing)
admin.site.register(NutritionPricing)
admin.site.register(SportHistoryPricing)
