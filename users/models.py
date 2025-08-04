#ya zahra
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from users.helpers import upload_to_role_based_path,validate_iran_home_phone

# Create your models here.

class BaseUser(AbstractUser):
    ROLE_CHOICE=[
        ("receptionist", ("Receptionist")),
        ("coach", ("Coach")),
        ("manager", ("Manager")),
        ("athlete",("Athelete"))
    
    ]
    role=models.CharField(max_length=20,choices=ROLE_CHOICE,default='athlete')

    def __str__(self):
        return self.username+'_'+self.role
    
    
class MidUser(BaseUser):
    STATUS_CHOICE=[
        ('ac','active'),
        ('inac','inactive'),
        ('ex','expired')
    ]
    address=models.TextField()
    phone_number=PhoneNumberField(region="IR")
    home_number=models.CharField(max_length=11,validators=[validate_iran_home_phone])
    father_name=models.CharField(verbose_name='father name',max_length=100)
    age=models.PositiveSmallIntegerField()
    image=models.ImageField(upload_to=upload_to_role_based_path,null=True,blank=True)
    balance_rial=models.DecimalField(verbose_name='balance',max_digits=15,decimal_places=0)
    status=models.CharField(max_length=4,choices=STATUS_CHOICE)

class Coach(MidUser):
    pass

class Athlete(MidUser):
    classes=models.ManyToManyField('training.Class',blank=True,null=True,related_name='athletes')
    coachs=models.ManyToManyField(Coach,through='SportHistory',related_name='athletes',blank=True,null=True)
    wieght=models.PositiveSmallIntegerField()
    height=models.PositiveSmallIntegerField()

class Manager(BaseUser):
    pass

class Reseption(MidUser):
    pass

class SportHistory(models.Model):
    athlete=models.ForeignKey(Athlete,on_delete=models.CASCADE,related_name='sport_historys')
    coach=models.ForeignKey(Coach,on_delete=models.SET_NULL,null=True,related_name='users_coaching')
    start_date=models.DateField(blank=True,null=True)
    end_date=models.DateField(null=True,blank=True)
    confirmation_coach=models.BooleanField(default=False)
    balance_for_coaching_rial=models.DecimalField(verbose_name='balance for coaching(rial)',max_digits=15,decimal_places=0)

    def __str__(self):
        return f'{self.athlete.username}_{self.coach.username}_{self.start_date}'

class WorkHistory(models.Model):
    user=models.ForeignKey(MidUser,on_delete=models.CASCADE,blank=True,related_name='work_histories')
    activity_type=models.CharField(max_length=50)
    activity_description=models.TextField(verbose_name='activity description(not required)',blank=True,null=True)
    start_activity=models.DateField()
    end_activity=models.DateField()
    lastest_salary_rial=models.DecimalField(verbose_name='lastes salary(rial)',max_digits=15,decimal_places=0)
    

    def __str__(self):
        return f'{self.user}_{self.activity_type}_{self.end_activity.year}'


class Message(models.Model):
    sender=models.ForeignKey(MidUser,on_delete=models.SET_NULL,null=True,related_name='')
    reciver=models.ForeignKey(MidUser,on_delete=models.CASCADE,related_name='')