from django.apps import AppConfig


class MembershipsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.memberships'

    def ready(self):
        from .signals import handle_order_and_order_item