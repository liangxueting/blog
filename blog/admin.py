from django.contrib import admin

# Register your models here.
from blog import models

admin.site.register(models.Member)
admin.site.register(models.Web)
admin.site.register(models.Article)
admin.site.register(models.Comment)