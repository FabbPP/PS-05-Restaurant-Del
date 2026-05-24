from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.enums import InvoiceType, PaymentMethod
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_non_empty


class Invoice(TimeStampedModel):
    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE, related_name="invoice")
    document_type = models.CharField(max_length=20, choices=InvoiceType.choices)
    document_number = models.CharField(max_length=30, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    is_paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(total_amount__gte=Decimal("0.00")), name="invoice_total_non_negative"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.document_number)
        if self.total_amount < 0:
            raise ValidationError("El total no puede ser negativo.")

    def __str__(self) -> str:
        return f"{self.document_type} {self.document_number}"

# Create your models here.
