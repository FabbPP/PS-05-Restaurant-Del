from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_int_range, validate_non_negative_int, validate_positive_int


class StockItem(TimeStampedModel):
    product = models.OneToOneField("catalog.Product", on_delete=models.CASCADE, related_name="stock")
    quantity = models.PositiveIntegerField(default=0, validators=[validate_non_negative_int])
    low_stock_threshold = models.PositiveIntegerField(default=5, validators=[validate_positive_int])

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gte=0), name="stock_quantity_non_negative"),
            models.CheckConstraint(condition=models.Q(quantity__lte=99999), name="stock_quantity_max"),
            models.CheckConstraint(condition=models.Q(low_stock_threshold__gt=0), name="stock_threshold_gt_zero"),
            models.CheckConstraint(condition=models.Q(low_stock_threshold__lte=9999), name="stock_threshold_max"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_int_range(self.quantity, 0, 99999)
        validate_int_range(self.low_stock_threshold, 1, 9999)

    def __str__(self) -> str:
        return f"{self.product.name} ({self.quantity})"


class StockMovement(TimeStampedModel):
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name="movements")
    delta = models.IntegerField()
    reason = models.CharField(max_length=120)

    def clean(self) -> None:
        super().clean()
        if self.delta is None:
            raise ValidationError("Delta requerido.")
        validate_positive_int(abs(self.delta))

    def __str__(self) -> str:
        return f"{self.item.product.name}: {self.delta}"

# Create your models here.
