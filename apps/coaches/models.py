from apps.basicusers.models import MidUser
# Create your models here.
class Coach(MidUser):
    def save(self, *args, **kwargs):
        self.role = 'coach'
        super().save(*args, **kwargs)