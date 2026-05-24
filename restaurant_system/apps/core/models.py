from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models


class TimeStampedModel(models.Model):
    """Base model with audit timestamps and strong validation on save."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:  # type: ignore[override]
        # Critical: enforce validation on every save to prevent corrupt data.
        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        # Subclasses should extend; keep base clean for explicitness.
        super().clean()

    def validate_unique(self, exclude=None) -> None:  # type: ignore[override]
        try:
            super().validate_unique(exclude=exclude)
        except ValidationError as exc:  # pragma: no cover - surface exact error
            raise exc

# Create your models here.
