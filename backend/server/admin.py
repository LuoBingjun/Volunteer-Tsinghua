from django.contrib import admin
from server import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.ApplyRecord)
admin.site.register(models.Project)
