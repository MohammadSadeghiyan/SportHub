from apps.basicusers.models import MidUser
# Create your models here.

class Receptionist(MidUser):
    def save(self, *args, **kwargs):
        self.role = 'receptionist'
        super().save(*args, **kwargs)

