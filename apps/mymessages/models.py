from django.db import models
from apps.basicusers.models import MidUser
from shortuuidfield import ShortUUIDField
# Create your models here.

class Mymessage(models.Model):
    READ_STATUS_CHOICE=(
        ('r','read'),
        ('n','not read')
    )
    public_id=ShortUUIDField(editable=False,unique=True)
    sender=models.ForeignKey(MidUser,on_delete=models.SET_NULL,null=True,related_name='send_messages')
    reciver=models.ForeignKey(MidUser,on_delete=models.CASCADE,related_name='recived_messages')
    titel=models.CharField(max_length=100)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    read_status=models.CharField(max_length=1,choices=READ_STATUS_CHOICE,default='n')

    def __str__(self):
        return f'{self.sender.public_id}_{self.reciver.public_id}'

