from django.db import models

# Create your models here.

class Report(models.Model):
    TYPE_CHOICE=[
        ('year','YEAR'),
        ('month','Month'),
        ('year','Year')
    ]
    type=models.CharField(max_length=5,choices=TYPE_CHOICE)
    date=models.DateTimeField(auto_now_add=True)
    total_sale=models.DecimalField(max_digits=21,decimal_places=0)
    total_payment=models.DecimalField(max_digits=15,decimal_places=0)
    total_reserve=models.PositiveIntegerField()
    active_user=models.PositiveIntegerField()
    inactive_user=models.PositiveIntegerField()
    expired_user=models.PositiveIntegerField()

    def __str__(self):
        return f'{self.pk}_{self.type}'