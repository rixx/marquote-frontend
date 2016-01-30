from django.contrib import admin

from . import models


admin.site.register(models.Project)
admin.site.register(models.Sequence)
admin.site.register(models.Word)
