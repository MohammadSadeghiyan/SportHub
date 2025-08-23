from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .helpers import upload_to_role_based_path,validate_iran_home_phone
from django.utils.translation import gettext_lazy as _
from shortuuidfield import ShortUUIDField

# Create your models here.

class BaseUser(AbstractUser):
    ROLE_CHOICE=[
        ("receptionist", "Receptionist"),
        ("coach", "Coach"),
        ("manager", "Manager"),
        ("athlete","Athelete"),
        ('admin','Admin')
    
    ]
    role=models.CharField(max_length=20,choices=ROLE_CHOICE,default='athlete')
    public_id = ShortUUIDField(unique=True, editable=False)
    def __str__(self):
        return self.username+'_'+self.get_role_display()
    
    
class MidUser(BaseUser):
    STATUS_CHOICE=[
        ('ac',_('active')),
        ('inac',_('inactive')),
        ('ex',_('expired'))
    ]
    home_address=models.TextField(blank=True,null=True)
    phone_number=PhoneNumberField(region="IR",blank=True,null=True)
    home_number=models.CharField(max_length=11,validators=[validate_iran_home_phone],blank=True,null=True)
    father_name=models.CharField(verbose_name='father name',max_length=100,blank=True,null=True)
    age=models.PositiveSmallIntegerField(null=True)
    image=models.ImageField(upload_to=upload_to_role_based_path,null=True,blank=True)
    balance_rial=models.DecimalField(verbose_name='balance(rial)',max_digits=12,decimal_places=0,default=0,blank=True)
    status=models.CharField(max_length=4,choices=STATUS_CHOICE,default='ac')
