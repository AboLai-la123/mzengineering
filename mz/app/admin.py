from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserTable)
admin.site.register(Order)
admin.site.register(Violation)
admin.site.register(Address)
admin.site.register(Object)