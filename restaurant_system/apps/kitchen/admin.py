from django.contrib import admin

from apps.kitchen.models import KitchenTicket


@admin.register(KitchenTicket)
class KitchenTicketAdmin(admin.ModelAdmin):
    list_display = ("order", "status", "started_at", "completed_at")

# Register your models here.
