from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee, Pay, Setter

admin.site.register(Employee)
admin.site.register(Pay)
admin.site.register(Setter)
