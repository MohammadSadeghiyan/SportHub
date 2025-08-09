from django.db import models
from apps.basicusers.models import MidUser
# Create your models here.

class WorkHistory(models.Model):
    user=models.ForeignKey(MidUser,on_delete=models.CASCADE,blank=True,related_name='work_histories')
    activity_type=models.CharField(max_length=50)
    activity_description=models.TextField(verbose_name='activity description(not required)',blank=True,null=True)
    start_activity=models.DateField()
    end_activity=models.DateField()
    lastest_salary_rial=models.DecimalField(verbose_name='lastes salary(rial)',max_digits=9,decimal_places=0)
    

    def __str__(self):
        return f'{self.user}_{self.activity_type}_{self.end_activity.year}'

