from django.contrib import admin

# Register your models here.
from localhandsapp.models import Scooper, Customer, Driver, Task

admin.site.register(Scooper)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Task)
