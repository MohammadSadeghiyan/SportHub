from .models import ClassItemPricing,ClassPricing,MembershipPricing,SportHistoryPricing,NutritionPricing
from rest_framework.exceptions import ValidationError
from django.db import transaction

class BasePricingService:
    model = None
    unique_fields = []

    @classmethod
    def _check_exists(cls, exclude_id=None, **filters):
        qs = cls.model.objects
        if exclude_id:
            qs = qs.exclude(public_id=exclude_id)
        if qs.filter(**filters).exists():
            raise ValidationError({'pricing': 'A pricing with these details already exists.'})

    @classmethod
    def create(cls, serializer):
        filters = {f: serializer.validated_data.get(f) for f in cls.unique_fields}
        cls._check_exists(**filters)

    @classmethod
    def update(cls, serializer, instance):
        filters = {
            f: serializer.validated_data.get(f, getattr(instance, f))
            for f in cls.unique_fields
        }
        cls._check_exists(exclude_id=instance.public_id, **filters)


class ClassPricingService(BasePricingService):
    model = ClassItemPricing
    unique_fields = ['session_ref', 'start_start_date', 'end_start_date']

    @classmethod
    def create(cls, serializer):
        items = serializer.validated_data.pop('items')
        with transaction.atomic():
            serializer.instance = class_pricing = ClassPricing.objects.create()
            for item in items:
                cls._check_exists(
                    session_ref=item.get('session_ref'),
                    end_start_date__gte=item.get('start_start_date'),
                    max_capacity__gte= serializer.validated_data.get('min_capacity')

                )
                ClassItemPricing.objects.create(**item, pricing=class_pricing)

    @classmethod
    def delete(cls, instance):
        instance.items.all().delete()
        instance.delete()


class ClassItemPricingService(BasePricingService):
    model = ClassItemPricing
    unique_fields = [
        'session_ref', 'start_start_date', 'end_start_date',
        'min_capacity', 'max_capacity'
    ]

    @classmethod
    def update(cls, serializer, instance):
        filters = {
            'session_ref': serializer.validated_data.get('session_ref', instance.session_ref),
            'end_start_date__gte': serializer.validated_data.get('start_start_date', instance.start_start_date),
            'max_capacity__gte': serializer.validated_data.get('min_capacity', instance.min_capacity),
        }
        cls._check_exists(exclude_id=instance.public_id, **filters)

class MembershipPricingService(BasePricingService):
    model = MembershipPricing
    unique_fields = ['type_name', 'start_start_date', 'end_start_date']

    @classmethod
    def create(cls, serializer):
        cls._check_exists(
            type_name=serializer.validated_data.get('type_name'),
            end_start_date__gte=serializer.validated_data.get('start_start_date')
        )

    @classmethod
    def update(cls, serializer, instance):
        cls._check_exists(
            exclude_id=instance.public_id,
            type_name=serializer.validated_data.get('type_name', instance.type_name),
            end_start_date__gte=serializer.validated_data.get('start_start_date',instance.start_start_date)
        )

class SportHistoryPricingService(BasePricingService):
    model=SportHistoryPricing
    unique_fields=['start_start_date','end_start_date']

    @classmethod
    def create(cls, serializer):
        cls._check_exists(
            end_start_date__gte=serializer.validated_data.get('start_start_date')
        )

    @classmethod
    def update(cls, serializer, instance):
        cls._check_exists(
            exclude_id=instance.public_id,
            end_start_date__gte=serializer.validated_data.get('start_start_date', instance.start_start_date)
        )

class NutritionPricingService(BasePricingService):
    model=NutritionPricing
    unique_fields=['start_start_date','end_start_date']

    @classmethod
    def create(cls, serializer):
        cls._check_exists(
            end_start_date__gte=serializer.validated_data.get('start_start_date'),
        )

    @classmethod
    def update(cls, serializer, instance):
        cls._check_exists(
            exclude_id=instance.public_id,
            end_start_date__gte=serializer.validated_data.get('start_start_date',instance.start_start_date),
        )