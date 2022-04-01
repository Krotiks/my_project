from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Ad)

admin.site.register(models.Comment)

@admin.register(models.Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish', 'ad_types')
    list_filter = ('ad_types', 'created')
    search_fields = ('title', 'text')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('publish', 'ad_types')

