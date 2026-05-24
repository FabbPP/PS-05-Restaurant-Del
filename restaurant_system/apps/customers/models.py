from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_non_empty, validate_phone


class Customer(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customer_profile",
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, validators=[validate_phone])

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.name)
        if self.email:
            self.email = self.email.lower()
        validate_phone(self.phone)

    def __str__(self) -> str:
        return self.name


class Address(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    reference = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField(default=False)

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.line1)
        validate_non_empty(self.city)

    def __str__(self) -> str:
        return f"{self.line1}, {self.city}"

# Create your models here.
