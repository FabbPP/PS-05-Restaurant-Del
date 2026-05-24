from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.core.enums import CourierStatus
from apps.core.models import TimeStampedModel
from apps.core.enums import UserRole
from apps.core.validators import validate_decimal_range, validate_int_range, validate_non_empty, validate_phone


class Courier(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courier_profile")
    is_available = models.BooleanField(default=True)

    def clean(self) -> None:
        super().clean()
        if self.user.role != UserRole.COURIER:
            raise ValidationError("El usuario asignado no tiene rol de repartidor.")

    def __str__(self) -> str:
        return self.user.username


class DeliveryInfo(TimeStampedModel):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="delivery_info")
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=15, validators=[validate_phone])
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal("0.00"))
    estimated_time_min = models.PositiveIntegerField()
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True)
    courier_status = models.CharField(
        max_length=20, choices=CourierStatus.choices, default=CourierStatus.ASSIGNED, blank=True
    )

    class Meta:
        constraints = [
            models.CheckConstraint(condition=Q(distance_km__gte=0), name="delivery_distance_non_negative"),
            models.CheckConstraint(condition=Q(distance_km__lte=Decimal("15.00")), name="delivery_distance_max"),
            models.CheckConstraint(condition=Q(estimated_time_min__gte=5), name="delivery_time_min"),
            models.CheckConstraint(condition=Q(estimated_time_min__lte=180), name="delivery_time_max"),
            models.CheckConstraint(condition=Q(delivery_fee__gte=0), name="delivery_fee_non_negative"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.address)
        validate_phone(self.phone)
        if self.distance_km is None:
            raise ValidationError("Distancia requerida.")
        validate_decimal_range(self.distance_km, Decimal("0.00"), Decimal("15.00"))
        if self.estimated_time_min is None:
            raise ValidationError("Tiempo estimado requerido.")
        validate_int_range(self.estimated_time_min, 5, 180)
        if self.courier_status in {CourierStatus.ON_ROUTE, CourierStatus.DELIVERED} and not self.courier:
            raise ValidationError("Se requiere repartidor para este estado.")

    def __str__(self) -> str:
        return f"Delivery {self.order_id}"

# Create your models here.
