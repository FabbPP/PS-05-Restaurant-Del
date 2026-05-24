from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.enums import KitchenStatus
from apps.core.models import TimeStampedModel


class KitchenTicket(TimeStampedModel):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="kitchen_ticket")
    status = models.CharField(max_length=20, choices=KitchenStatus.choices, default=KitchenStatus.QUEUED)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def clean(self) -> None:
        super().clean()
        if self.completed_at and not self.started_at:
            raise ValidationError("No se puede completar sin iniciar.")
        if self.started_at and self.completed_at and self.completed_at < self.started_at:
            raise ValidationError("La fecha de fin no puede ser anterior al inicio.")

    def __str__(self) -> str:
        return f"Ticket cocina #{self.order_id}"

# Create your models here.
