from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Contact)
admin.site.register(Address)
admin.site.register(PhoneNumber)
admin.site.register(Date)