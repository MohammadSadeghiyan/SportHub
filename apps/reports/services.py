from apps.basicusers.models import MidUser
from apps.managers.models import Manager
from apps.reservations.models import Reservation
from apps.orders.models import Order,MembershipItem
from decimal import Decimal
from django.db.models import Prefetch
from apps.payments.models import RecpetionistPayment
from .helpers import set_start_date
from .models import Report

class ReportService:

    def __init__(self,data,user=None):
        self.end_date=data.get('end_date',None)#None could happened when update call
        self.type_name=data.get('type_name',None)#None could happend when update call
        self.name=data.get('name',None)#None could happened when update call 
        self.user=user
        if self.end_date and self.type_name:
            self.start_date=set_start_date(end_date=self.end_date,type_name=self.type_name)
    
    def make_report(self):

        other_data=self.calculate_report_data(self.start_date,self.end_date)
        report=Report(**other_data,start_date=self.start_date,end_date=self.end_date,name=self.name,type_name=self.type_name)
        report.save()
        manager=Manager.objects.filter(pk=self.user.pk).first()
        manager.save()
        return report

    def calculate_report_data(self):
        return{
            "active_user":self.count_active_user(),
            "inactive_user":self.count_inactive_user(),
            "expired_user":self.count_expired_user(),
            "total_reserve":self.count_total_reserve(),
            "total_sale":self.calculate_total_sale(),
            "total_payment":self.calculate_total_payment()

        }
    
    def count_active_user(self):
        active_user=MidUser.objects.filter(last_login__gte=self.start_date).exclude(role='receptionist')\
                                                                            .filter(memberships__status=True)\
                                                                                .distinct().count()
        return active_user

    def count_inactive_user(self):

        inactive_user=0
        inactive_user=MidUser.objects.filter(last_login__lt=self.start_date).exclude(role='receptionist')\
                                                                    .exclude(memberships__status=True)\
                                                                        .distinct().count()
        return inactive_user   
        
    def count_expired_user(self):
        expired_user=0
        expired_user=MidUser.objects.filter(date_joined__gte=self.start_date,date_joined__lte=self.end_date)\
                                        .exclude(role='receptionist').exclude(memberships__status=True)\
                                           .distinct().count()
        return expired_user


    def count_total_reserve(self):
        total_rervers_count=Reservation.objects.filter(date__gte=self.start_date,date__lte=self.end_date).count()
        return total_rervers_count


    def calculate_total_sale(self):
        membership_order_items=MembershipItem.objects.filter(order__status='paid')\
                                                        .filter(order__registered_at__gte=self.start_date
                                                                ,order__registered_at__lte=self.end_date)\
                                                                    .values('order','price')
        total=Decimal(0)

        membership_orders=[]
        for membership_item in membership_order_items:
            membership_orders.append(membership_item['order'])
            total+=membership_item['price']



        orders_price=Order.objects.exclude(pk__in=membership_orders).filter(status='paid')\
                                                                        .filter(registered_at__gte=self.start_date
                                                                                ,registered_at__lte=self.end_date)\
                                                                            .values_list('price',flat=True)
        for price in orders_price:
            total+=price*.1

        return total

    def calculate_total_payment(self):
        price_payments=RecpetionistPayment.objects.filter(date__gte=self.start_date,date__lte=self.end_date)\
                                                    .values_list('salary',flat=True)
        if not price_payments:return Decimal(0) 
        return Decimal(sum(price_payments))

    def update_report(self,instance):
        return self.update(instance)
     
    
    def update(self,instance):
        flag=False
        if (self.end_date or self.type_name) and ((self.end_date and self.end_date!=instance.end_date)\
                                                or (self.type_name and self.type_name!=instance.type_name)):
            flag=True
            if self.end_date:instance.end_date=self.end_date 
            else : self.end_date=instance.end_date
            if self.type_name:instance.type_name=self.type_name
            else:self.type_name=instance.type_name
            self.start_date=set_start_date(end_date=self.end_date,type_name=self.type_name)
            instance.start_date=self.start_date
            other_data=self.calculate_report_data()
            for field_name, value in other_data.items():
                setattr(instance, field_name, value)
        if self.name:
            flag=True
            instance.name=self.name
            
        if flag:instance.save()
        return instance
    
    






