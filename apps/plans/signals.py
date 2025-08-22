from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NutritionPlan
from apps.orders.models import Order,NutritionPlanItem

@receiver(post_save,sender=NutritionPlan)
def handel_order_and_order_item(sender,instance,created,**kwargs):
        print('we save')
        athlete=instance.athlete
        pended_order=Order.objects.filter(user=athlete,status='pending')
        if pended_order.exists():
            pended_order=pended_order.first()
            pended_order.price+=instance.salary_rial
            pended_order.save()
        else:
            pended_order=Order.objects.create(user=athlete,price=instance.salary_rial)
            
        if created :
            NutritionPlanItem.objects.create(order=pended_order,plan=instance,price=instance.salary_rial)
        else:
            nutritionplan=NutritionPlanItem.objects.get(plan=instance,order=pended_order)
            nutritionplan.price=instance.salary_rial
            nutritionplan.save()
    
        
    
