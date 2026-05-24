from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.enums import UserRole
from apps.core.validators import validate_non_empty, validate_phone


class User(AbstractUser):
    """Custom user with role and phone validation."""

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER,
    )
    phone = models.CharField(max_length=15, blank=True, validators=[validate_phone])

    def clean(self) -> None:
        super().clean()
        validate_non_empty(self.username)
        if self.email:
            self.email = self.email.lower()
        if self.phone:
            validate_phone(self.phone)

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"

# Create your models here.
