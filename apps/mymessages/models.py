from django.db import models
from apps.basicusers.models import MidUser
# Create your models here.

class Mymessage(models.Model):
    sender=models.ForeignKey(MidUser,on_delete=models.SET_NULL,null=True,related_name='send_messages')
    reciver=models.ForeignKey(MidUser,on_delete=models.CASCADE,related_name='recived_messages')
    titel=models.CharField(max_length=100)
    text=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


