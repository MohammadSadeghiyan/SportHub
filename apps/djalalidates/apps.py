from django.apps import AppConfig

class DjalalidatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.djalalidates'

    def ready(self):
        import apps.djalalidates.schema_extensions