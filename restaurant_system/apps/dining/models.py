from __future__ import annotations

from django.db import models

from apps.core.enums import TableStatus
from apps.core.models import TimeStampedModel
from apps.core.validators import validate_int_range


class Table(TimeStampedModel):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=TableStatus.choices, default=TableStatus.FREE)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(number__gte=1), name="table_number_gte_one"),
            models.CheckConstraint(condition=models.Q(number__lte=200), name="table_number_lte_200"),
            models.CheckConstraint(condition=models.Q(capacity__gte=1), name="table_capacity_gte_one"),
            models.CheckConstraint(condition=models.Q(capacity__lte=50), name="table_capacity_lte_50"),
        ]

    def clean(self) -> None:
        super().clean()
        validate_int_range(self.number, 1, 200)
        validate_int_range(self.capacity, 1, 50)

    def __str__(self) -> str:
        return f"Mesa {self.number}"

# Create your models here.
