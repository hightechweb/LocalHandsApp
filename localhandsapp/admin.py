from django.contrib import admin

# Rename django admin
from django.utils.translation import ugettext as _
admin.site.site_header = _(u"LocalHands Admin Panel")
# admin.site.index_title = _(u"Subtitle")

# Register your models here.
from localhandsapp.models import Scooper, Customer, Driver, Task, Order, OrderDetails
admin.site.register(Scooper)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Task)
admin.site.register(Order)
admin.site.register(OrderDetails)
