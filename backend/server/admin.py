from django.contrib import admin
from server import models

# Register your models here.
admin.site.register(models.WxUser)
admin.site.register(models.WebUser)
admin.site.register(models.ApplyRecord)
admin.site.register(models.Project)
admin.site.register(models.SignProject)
admin.site.register(models.SignRecord)
admin.site.register(models.JoinRecord)
admin.site.register(models.Job)
