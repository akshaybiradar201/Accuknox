from django.contrib import admin
from .models import CustomUser, Request
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Request)