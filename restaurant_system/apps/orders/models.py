from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.enums import OrderStatus, OrderType
from apps.core.models import TimeStampedModel
from apps.core.utils import quantize_money
from apps.core.validators import validate_decimal_range, validate_int_range


class Order(TimeStampedModel):
    order_type = models.CharField(max_length=20, choices=OrderType.choices)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    table = models.ForeignKey("dining.Table", on_delete=models.PROTECT, null=True, blank=True)
    customer = models.ForeignKey("customers.Customer", on_delete=models.PROTECT, null=True, blank=True)
    waiter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="served_orders",
    )
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(total__gte=0), name="order_total_non_negative"),
        ]

    def clean(self) -> None:
        super().clean()
        if self.order_type == OrderType.DINE_IN and not self.table:
            raise ValidationError("Las órdenes de mesa requieren una mesa asignada.")
        if self.order_type == OrderType.DELIVERY and self.table:
            raise ValidationError("Las órdenes delivery no deben tener mesa.")
        if self.order_type == OrderType.DELIVERY and not self.customer:
            raise ValidationError("Las órdenes delivery requieren cliente.")
        if self.total < 0:
            raise ValidationError("El total no puede ser negativo.")
        self.total = quantize_money(self.total)

    def __str__(self) -> str:
        return f"Orden #{self.pk} - {self.get_order_type_display()}"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(quantity__gt=0), name="order_item_qty_gt_zero"),
            models.CheckConstraint(condition=models.Q(quantity__lte=100), name="order_item_qty_max"),
            models.CheckConstraint(condition=models.Q(unit_price__gt=0), name="order_item_price_gt_zero"),
            models.CheckConstraint(condition=models.Q(subtotal__gte=0), name="order_item_subtotal_non_negative"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_int_range(self.quantity, 1, 100)
        validate_decimal_range(self.unit_price, Decimal("0.01"), Decimal("9999.99"))
        expected = quantize_money(Decimal(self.quantity) * self.unit_price)
        if quantize_money(self.subtotal) != expected:
            raise ValidationError("El subtotal no coincide con cantidad x precio.")
        self.subtotal = expected

    def __str__(self) -> str:
        return f"{self.product.name} x{self.quantity}"


class OrderStatusHistory(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_history")
    from_status = models.CharField(max_length=20, choices=OrderStatus.choices)
    to_status = models.CharField(max_length=20, choices=OrderStatus.choices)

    def clean(self) -> None:
        super().clean()
        if self.from_status == self.to_status:
            raise ValidationError("El estado nuevo debe ser diferente al anterior.")

    def __str__(self) -> str:
        return f"{self.order_id}: {self.from_status} -> {self.to_status}"

# Create your models here.
