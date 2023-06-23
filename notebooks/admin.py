from django.contrib import admin
from notebooks import models

admin.site.register(models.Notebook)
admin.site.register(models.Notes)
admin.site.register(models.Tasks)
admin.site.register(models.TaskGroup)
