from django.db import models
from shortuuidfield import ShortUUIDField
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Mysession(models.Model):
    DAYS_OF_WEEK = (
    ('mon', 'Monday'),
    ('tue', 'Tuesday'),
    ('wed', 'Wednesday'),
    ('thu', 'Thursday'),
    ('fri', 'Friday'),
    ('sat', 'Saturday'),
    ('sun', 'Sunday'),
    )
    public_id=ShortUUIDField(editable=False,unique=True)
    days = ArrayField(
        models.CharField(max_length=3, choices=DAYS_OF_WEEK),
        default=list,
        blank=True
    )
    start_time=models.TimeField()
    end_time=models.TimeField()

    def __str__(self):
        return f'{self.public_id}_{self.days}'
