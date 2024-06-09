from django.contrib import admin

# Register your models here.
from .models import Manager,Employee,Component,Administrator,Details

admin.site.register(Manager)
admin.site.register(Administrator)
admin.site.register(Details)
admin.site.register(Employee)
admin.site.register(Component)
