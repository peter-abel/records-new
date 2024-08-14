from django.contrib import admin
from .models import NewOrder, Status,Payment
# Register your models here.

admin.site.register(NewOrder)
admin.site.register(Status)
admin.site.register(Payment)
