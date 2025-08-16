from .models import *
from .permissions import *
from rest_framework import viewsets,permissions
from .serializers import *
from .filters import *
from .services import *
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from .api_params import *
# Create your views here.

class ClassPricingViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return ClassPricing.objects.all().prefetch_related(Prefetch('session_ref',queryset=Mysession.objects.all().only('public_id')))
    
    serializer_class=ClassPricingSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerNoUpdatePermission]
    lookup_field='public_id'

    def perform_create(self, serializer):
        ClassPricingService.create(serializer)
        

    def perform_destroy(self, instance):
        ClassItemPricing.delete(instance)

@extend_schema(
    parameters=CLASS_ITEM_PRICING_ITEMS
)
class ClassItemPricingViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return ClassItemPricing.objects.all()
    
    serializer_class=ClassItemPricingSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerNoCreatePermission]
    filterset_classes=ClassItemPricingFilter

    def perform_update(self, serializer):
        instance=self.get_object()
        ClassItemPricingService.update(serializer,instance)
        return super().perform_update(serializer)

@extend_schema(
     parameters=MEMBERSHIP_PRICING_ITEMS
 )   
class MembershipPricingViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return MembershipPricing.objects.all()
    
    serializer_class=MembershipPricingSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionistReadOnlyPermission]
    filterset_classes=MembershipPricingFilter
    lookup_field='public_id'

    def perform_create(self, serializer):
        MembershipPricingService.create(serializer)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        instance=self.get_object()
        MembershipPricingService.update(serializer,instance)
        return super().perform_update(serializer)
    
@extend_schema(
    parameters=SPORTHISTORY_PRICING_ITEMS
)
class SportHistoryPricingViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return SportHistoryPricing.objects.all()
    
    serializer_class=SportHistoryPricingSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionistReadOnlyPermission]
    filterset_classes=SportHistoryPricingFilter
    lookup_field='public_id'

    def perform_create(self, serializer):
        SportHistoryPricingService.create(serializer)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        instance=self.get_object()
        SportHistoryPricingService.update(serializer,instance)
        return super().perform_update(serializer)
    
@extend_schema(
    parameters=NUTRITION_PRICING_ITEMS
)
class NutritionPricingViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return NutritionPricing.objects.all()
    
    serializer_class=NutritionPricingSerializer
    permission_classes=[permissions.IsAuthenticated,ManagerOrReceptionistReadOnlyPermission]
    lookup_field='public_id'
    filterset_classes=NutritionPricingFilter

    def perform_create(self, serializer):
        NutritionPricingService.create(serializer)
        return super().perform_create(serializer)
    
    def perform_update(self, serializer):
        instance=self.get_object()
        NutritionPricingService.update(serializer,instance)
        return super().perform_update(serializer)
    

