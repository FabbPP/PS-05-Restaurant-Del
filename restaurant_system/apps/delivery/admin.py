from django.contrib import admin

from apps.delivery.models import Courier, DeliveryInfo


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ("user", "is_available")


@admin.register(DeliveryInfo)
class DeliveryInfoAdmin(admin.ModelAdmin):
    list_display = ("order", "distance_km", "delivery_fee", "estimated_time_min", "courier_status")

# Register your models here.
