from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.enums import PaymentMethod
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_positive_decimal


class Payment(TimeStampedModel):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="payment")
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(amount__gte=Decimal("0.00")), name="payment_amount_non_negative"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_positive_decimal(self.amount)
        if self.order and self.amount < self.order.total:
            raise ValidationError("El monto pagado no cubre el total.")

    def __str__(self) -> str:
        return f"Pago #{self.order_id}"

# Create your models here.
