from django.contrib import admin

# Register your models here.
from localhandsapp.models import Scooper, Customer, Driver

admin.site.register(Scooper)
admin.site.register(Customer)
admin.site.register(Driver)
