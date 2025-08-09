from django.apps import AppConfig


class BasicusersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.basicusers'

    def ready(self):
        from .signals import set_image_name_base_username