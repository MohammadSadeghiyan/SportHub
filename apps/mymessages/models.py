from django.db import models
from apps.basicusers.models import BaseUser
from shortuuidfield import ShortUUIDField
# Create your models here.

class Mymessage(models.Model):
    READ_STATUS_CHOICE=(
        ('r','read'),
        ('n','not read')
    )
    public_id=ShortUUIDField(editable=False,unique=True)
    sender=models.ForeignKey(BaseUser,on_delete=models.SET_NULL,null=True,related_name='send_messages')
    reciver=models.ForeignKey(BaseUser,on_delete=models.CASCADE,related_name='recived_messages')
    titel=models.CharField(max_length=100)
    text=models.TextField()
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    created_time=models.TimeField(auto_now_add=True)
    updated_time=models.TimeField(auto_now=True)
    read_status=models.CharField(max_length=1,choices=READ_STATUS_CHOICE,default='n')
    read_date=models.DateField(null=True)
    read_time=models.TimeField(null=True)
    def __str__(self):
        return f'{self.sender.public_id}_{self.reciver.public_id}'

