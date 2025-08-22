from django.apps import AppConfig


class SporthistoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sporthistories'

    def ready(self):
        from .signals import handel_order_and_order_item