from django.db.models.signals import post_delete,post_save
from django.dispatch import receiver
from .models import Athlete
from django.core.cache import cache

@receiver([post_delete,post_save],sender=Athlete)
def invalidate_athlete_cache(sender,instance,**kwargs):

    cache.delete_patterns('*athlete-list*')
