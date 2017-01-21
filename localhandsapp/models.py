from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Scooper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scooper')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='scooper_logo/', blank=True)

    # Required to render object to views...
    def __str__(self):
        # full_name = self.user.first_name + ' ' + self.user.last_name
        return self.user.get_full_name()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Task(models.Model):
    scooper = models.ForeignKey(Scooper)
    name = models.CharField(max_length=500, blank=False)
    short_description = models.CharField(max_length=500, blank=False)
    price = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    PENDING = 1
    PROCESSING = 2
    ONTHEWAY = 3
    DELIVERED  = 4

    STATUS_CHOICES = {
        (PENDING, "Pending"),
        (PROCESSING, "Started"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    }

    customer = models.ForeignKey(Customer)
    scooper = models.ForeignKey(Scooper)
    driver = models.ForeignKey(Driver, blank=True, null=True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)
    delivered_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details')
    task = models.ForeignKey(Task)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)
