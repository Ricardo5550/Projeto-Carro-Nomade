from django.contrib import admin
from myapp import models

# Register your models here.
admin.site.register(models.Client)
admin.site.register(models.RegisterRent)
admin.site.register(models.LogAuditoria)

class AutomovelImageInlineAdmin(admin.TabularInline):
    model = models.AutomovelImage
    extra = 0

class AutomovelAdmin(admin.ModelAdmin):
    inlines = [AutomovelImageInlineAdmin]

admin.site.register(models.Automovel, AutomovelAdmin)
