from rest_framework import serializers
from .models import *

class SporthistoryItemNestedSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='orders:sporthistory-item-detail',lookup_field='public_id',read_only=True)
    sporthistory=serializers.HyperlinkedRelatedField(view_name='sporthistories:sport-history-detail',lookup_field='public_id',read_only=True)
    class Meta:
        model=SportHistoryItem
        fields=['url','public_id','price','sporthistory']
        read_only_fields=('price','url','order','sporthistory','public_id')
        extra_kwargs = {
            'sporthistory': {'write_only': True}
        }

class SporthistoryItemSerializer(SporthistoryItemNestedSerializer):
  
    order=serializers.HyperlinkedRelatedField(view_name='orders:athlete-order-detail',lookup_field='public_id',read_only=True)
   
    class Meta(SporthistoryItemNestedSerializer.Meta):
        fields=SporthistoryItemNestedSerializer.Meta.fields+['order']
        read_only_fields=('price','url','order','sporthistory','public_id')


class MembershipItemNestedSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='orders:membership-item-detail',lookup_field='public_id',read_only=True)
    membership=serializers.SerializerMethodField()
    
    class Meta:
        model=MembershipItem
        fields=['url','price','public_id','membership']
        read_only_fields=('public_id','price','url')

        extra_kwargs = {
            'membership': {'write_only': True}
        }

    def get_membership(self,obj):
        request=self.context.get('request')
        if obj.order.user.role=='athlete':
            return request.build_absolute_uri(f'/api/athlete-memberships/{obj.membership.public_id}')
        return request.build_absolute_uri(f'/api/coach-memberships/{obj.membership.public_id}')

class MembershipItemSerializer(MembershipItemNestedSerializer):
    order=serializers.SerializerMethodField()
    class Meta(MembershipItemNestedSerializer.Meta):
        fields=MembershipItemNestedSerializer.Meta.fields+['order']
        read_only_fields=('public_id','url','price','membership','order')
    
    def get_order(self,obj):
        request=self.context.get('request')
        if obj.order.user.role=='athlete':
            return request.build_absolute_uri(f'/api/athlete-orders/{obj.public_id}')
        return request.build_absolute_uri(f'/api/coach-orders/{obj.public_id}')


class NutritoinPlanItemNestedSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='orders:nutrition-plan-item-detail',lookup_field='public_id',read_only=True)
    plan_url=serializers.HyperlinkedRelatedField(source='plan',view_name='plans:nutritionplan-detail',lookup_field='public_id',read_only=True)
    plan=serializers.SlugRelatedField(slug_field='public_id',queryset=NutritionPlan.objects.all())
    
    class Meta:
        model=NutritionPlanItem
        fields=['url','price','public_id','plan_url','plan']
        read_only_fields=('public_id','price','url','plan_url')

        extra_kwargs = {
            'plan': {'write_only': True}
        }

class NutritionPlanItmeSerializer(NutritoinPlanItemNestedSerializer):
    order=serializers.HyperlinkedRelatedField(view_name='orders:athlete-order-detail',lookup_field='public_id',read_only=True)
    class Meta(NutritoinPlanItemNestedSerializer.Meta):
        fields=NutritoinPlanItemNestedSerializer.Meta.fields+['order']
        read_only_fields=('public_id','price','url','plan_url','order')


class ReservationItemNestedSerializer(serializers.HyperlinkedModelSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='orders:membersipitem-detail',lookup_field='public_id',read_only=True)
    reservation_url=serializers.HyperlinkedRelatedField(source='reservation',view_name='reservations:reservation-detail',lookup_field='public_id',read_only=True)
    reservation=serializers.SlugRelatedField(slug_field='public_id',queryset=Reservation.objects.all())
    
    class Meta:
        model=ReservationItem
        fields=['url','price','public_id','reservation_url','reservation']
        read_only_fields=('public_id','price','url','reservation_url')

        extra_kwargs = {
            'reservation': {'write_only': True}
        }


class ReservationItemSerializer(ReservationItemNestedSerializer):
    order=serializers.HyperlinkedRelatedField(view_name='orders:athlete-order-detail',lookup_field='public_id',read_only=True)
    
    class Meta(ReservationItemNestedSerializer.Meta):
        fields=ReservationItemNestedSerializer.Meta.fields+['order']
        read_only_fields=('url','price','public_id','reservation_url','order')


class AbstractOrderSerializer(serializers.ModelSerializer):
    payments=serializers.HyperlinkedRelatedField(view_name='payments:payment-detail',lookup_field='public_id',read_only=True,many=True)
    membershipitem_items=MembershipItemNestedSerializer(many=True,read_only=True)
    class Meta:
        model=Order
        fields=['public_id','created_at','status','price','registered_at','membershipitem_items','payments']
        read_only_fields=('public_id','created_at','registered_at','membershipitem_items','payments')

        
class AthleteOrderSerailizer(serializers.HyperlinkedModelSerializer,AbstractOrderSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='orders:athlete-order-detail',lookup_field='public_id',read_only=True)
    sporthistoryitem_items=SporthistoryItemNestedSerializer(read_only=True,many=True)
    nutritionplanitem_items=NutritoinPlanItemNestedSerializer(read_only=True,many=True)
    reservationitem_items=ReservationItemNestedSerializer(read_only=True,many=True)
    user=serializers.HyperlinkedRelatedField(view_name='athletes:athlete-detail',lookup_field='public_id',read_only=True)
    
    class Meta(AbstractOrderSerializer.Meta):
        fields=AbstractOrderSerializer.Meta.fields+['url','user','sporthistoryitem_items','nutritionplanitem_items','reservationitem_items']
        read_only_fields=('public_id','created_at','registered_at','membershipitem_items','payments','url','sporthistoryitem_items',
                          'nutritionplanitem_items','reservationitem_items','user')

class CoachOrderSerializer(serializers.HyperlinkedModelSerializer,AbstractOrderSerializer):
    url=serializers.HyperlinkedIdentityField(view_name='orders:coach-order-detail',lookup_field='public_id',read_only=True)
    user=serializers.HyperlinkedRelatedField(view_name='coaches:coach-detail',lookup_field='public_id',read_only=True)

    class Meta(AbstractOrderSerializer.Meta):
        fields=AbstractOrderSerializer.Meta.fields+['url','user']
        read_only_fields=('public_id','created_at','registered_at','membershipitem_items','payments','url','user')



