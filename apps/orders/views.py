from rest_framework import viewsets,mixins,permissions,exceptions
from .models import *
from .permissions import *
from .filters import *
from .serializers import *
from django.db.models import Prefetch
from apps.memberships.models import Membership
from rest_framework.exceptions import ValidationError

class AthleteOrderViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):

    def get_queryset(self):
        user=self.request.user
        
        if user.role in ['manager','receptionist']:
            return Order.objects.filter(user__role='athlete')\
                        .select_related('user').prefetch_related(
                            Prefetch('sporthistoryitem_items',
                                queryset=SportHistoryItem.objects.all()))\
                                    .prefetch_related(
                                        Prefetch('membershipitem_items'
                                            ,queryset=MembershipItem.objects.all()))\
                                                .prefetch_related(
                                                    Prefetch('nutritionplanitem_items',
                                                        queryset=NutritionPlanItem.objects.all()))\
                                                            .prefetch_related(
                                                                Prefetch('reservationitem_items',
                                                                    queryset=ReservationItem.objects.all()))
        
        
        return Order.objects.filter(user__role='athlete',user__public_id=user.public_id)\
                    .select_related('user').prefetch_related(
                        Prefetch('sporthistoryitem_items',
                            queryset=SportHistoryItem.objects.all()))\
                                .prefetch_related(
                                    Prefetch('membershipitem_items'
                                        ,queryset=MembershipItem.objects.all()))\
                                            .prefetch_related(
                                                Prefetch('nutritionplanitem_items',
                                                    queryset=NutritionPlanItem.objects.all()))\
                                                        .prefetch_related(
                                                            Prefetch('reservationitem_items',
                                                                queryset=ReservationItem.objects.all()))
        
        
        
                                                        

    
    serializer_class=AthleteOrderSerailizer
    lookup_field='public_id'
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionReadOnlyOrAthlete]
    filterset_class=OrderFilter

    def perform_destroy(self, instance):
        if instance.status=='paid':
            raise ValidationError({'status paid':'this order status is paid .you can delete this order'})
        for membership_item in instance.membershipitem_items.all():
            membership=Membership.objects.get(public_id=membership_item.membership.public_id)  
            membership.delete()

        for sporthistory_item in instance.sporthistoryitem_items.all():
            sporthitory=SportHistory.objects.get(public_id=sporthistory_item.sporthisotry.public_id)
            sporthitory.delete()
        for reservation_item in instance.reservationitem_items.all():
            reservation=Reservation.objects.get(public_id=reservation_item.reservation.public_id)
            reservation.delete()
        for nutritionplan_item in instance.nutritionplanitem_items.all():
            plan=NutritionPlan.objects.get(public_id=nutritionplan_item.plan.public_id)
            plan.delete()
        instance.delete()

class CoachOrderViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):

    def get_queryset(self):
        user=self.request.user
        
        if user.role in ['manager','receptionist']:
            return Order.objects.filter(user__role='coach')\
                        .select_related('user').prefetch_related(
                            Prefetch('membershipitem_items'
                                ,queryset=MembershipItem.objects.all()))
        
        
        return Order.objects.filter(user__role='coach',user__public_id=user.public_id)\
                        .select_related('user').prefetch_related(
                            Prefetch('membershipitem_items'
                                ,queryset=MembershipItem.objects.all()))
        
        
    
    serializer_class=CoachOrderSerializer
    lookup_field='public_id'
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionReadOnlyOrCoach]
    filterset_class=OrderFilter

    

    def perform_destroy(self, instance):
        if instance.status=='paid':
            raise ValidationError({'status paid':'this order status is paid .you can delete this order'})
        for membership_item in instance.membershipitem_items.all():
            membership=Membership.objects.get(public_id=membership_item.membership.public_id)  
            membership.delete()
        instance.delete()
    
    

class MembershipItemViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):


    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return MembershipItem.objects.all().select_related('order__user')
        else :
            return MembershipItem.objects.filter(order__user__public_id=user.public_id).select_related('order__user')
    
    lookup_field='public_id'
    serializer_class=MembershipItemSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionistReadOnlyOrUser]
    filterset_class=MembershipItemFilter


    
    def perform_destroy(self, instance):
        if instance.order.status=='paid':
            raise exceptions.ValidationError({'order paid':'you can not delete order that paid it'})
        membership=Membership.objects.get(public_id=instance.membership.public_id)
        membership.delete()
        
class SportHistoryItemViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    

    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return SportHistoryItem.objects.all().select_related('order__user')
        else:
            return SportHistoryItem.objects.filter(order__user__public_id=user.public_id).select_related('order__user')
    

    lookup_field='public_id'
    serializer_class=SporthistoryItemSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionistReadOnlyOrUser]
    filterset_class=SportHistoryItemFilter


   
    
    def perform_destroy(self, instance):
        if instance.order.status=='paid':
            raise exceptions.ValidationError({'order paid':'you can not delete order that paid it'})
        sporthistory=SportHistory.objects.get(public_id=instance.sporthistory.public_id)
        sporthistory.delete()
    

class NutritionPlanItemViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    

    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return NutritionPlanItem.objects.all().select_related('order__user')
        else:
            return NutritionPlanItem.objects.filter(order__user__public_id=user.public_id).select_related('order__user')
    

    lookup_field='public_id'
    serializer_class=NutritionPlanItmeSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionistReadOnlyOrUser]
    filterset_class=NutritionPlanItemFilter


   
    
    def perform_destroy(self, instance):
        if instance.order.status=='paid':
            raise exceptions.ValidationError({'order paid':'you can not delete order that paid it'})
        nutrition_plan=NutritionPlan.objects.get(public_id=instance.plan.public_id)
        nutrition_plan.delete()
    


class ReservationItemViewSet(mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    

    def get_queryset(self):
        user=self.request.user
        if user.role in ['manager','receptionist']:
            return ReservationItem.objects.all().select_related('order__user')
        else:
            return ReservationItem.objects.filter(order__user__public_id=user.public_id).select_related('order__user')
    

    lookup_field='public_id'
    serializer_class=ReservationItemSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerReceptionistReadOnlyOrUser]
    filterset_class=ReservationItemFilter


   
    
    def perform_destroy(self, instance):
        if instance.order.status=='paid':
            raise exceptions.ValidationError({'order paid':'you can not delete order that paid it'})
        reservation=Reservation.objects.get(public_id=instance.reservation.public_id)
        reservation.delete()
    

