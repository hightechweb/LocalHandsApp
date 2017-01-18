from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Scooper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scooper')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='scooper_logo/', blank=False)

    # Required to render object to views...
    def __str__(self):
        full_name = self.user.first_name + ' ' + self.user.last_name
        return full_name
