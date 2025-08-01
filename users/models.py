from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from users.helpers import upload_to_role_based_path,validate_iran_home_phone
# Create your models here.

class BaseUser(AbstractUser):
    role_choice=[
        ("receptionist", ("Receptionist")),
        ("coach", ("Coach")),
        ("manager", ("Manager")),
        ("athlete",("Athelete"))
    
    ]
    role=models.CharField(max_length=20,choices=role_choice,default='athlete')

class MidUser(BaseUser):
    address=models.TextField()
    phone_number=PhoneNumberField(region="IR")
    home_number=PhoneNumberField(region='IR',validators=[validate_iran_home_phone])
    father_name=models.CharField(verbose_name='father name',max_length=100)
    age=models.SmallIntegerField()
    image=models.ImageField(upload_to=upload_to_role_based_path,null=True,blank=True)