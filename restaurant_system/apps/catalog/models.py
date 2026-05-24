from __future__ import annotations

from decimal import Decimal

from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_decimal_range, validate_non_empty


class Category(TimeStampedModel):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=200, blank=True)

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.name)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampedModel):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(price__gt=Decimal("0.00")), name="product_price_gt_zero"),
            models.CheckConstraint(condition=models.Q(price__lte=Decimal("9999.99")), name="product_price_max"),
            models.UniqueConstraint(fields=["category", "name"], name="unique_product_per_category"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.name)
        validate_decimal_range(self.price, Decimal("0.01"), Decimal("9999.99"))

    def __str__(self) -> str:
        return self.name

# Create your models here.
