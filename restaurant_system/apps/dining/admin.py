from django.contrib import admin

from apps.dining.models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "capacity", "status")
    list_filter = ("status",)

# Register your models here.
