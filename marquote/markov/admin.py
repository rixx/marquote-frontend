from django.contrib import admin

from . import models


admin.site.register(models.BaseProject)
admin.site.register(models.BaseSentence)
admin.site.register(models.Sentence)
admin.site.register(models.Word)
