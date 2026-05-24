from django.contrib import admin

from apps.inventory.models import StockItem, StockMovement


@admin.register(StockItem)
class StockItemAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "low_stock_threshold")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("item", "delta", "reason", "created_at")

# Register your models here.
