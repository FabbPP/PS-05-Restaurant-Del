from __future__ import annotations

import re
from decimal import Decimal
from typing import Iterable

from django.core.exceptions import ValidationError

PHONE_REGEX = re.compile(r"^\+?\d{9,15}$")


def validate_non_empty(value: str) -> None:
    if value is None or not str(value).strip():
        raise ValidationError("Este campo es obligatorio.")


def validate_positive_decimal(value: Decimal) -> None:
    if value is None or value <= 0:
        raise ValidationError("El valor debe ser mayor a 0.")


def validate_non_negative_int(value: int) -> None:
    if value is None or value < 0:
        raise ValidationError("El valor no puede ser negativo.")


def validate_positive_int(value: int) -> None:
    if value is None or value <= 0:
        raise ValidationError("El valor debe ser mayor a 0.")


def validate_int_range(value: int, min_value: int, max_value: int) -> None:
    if value is None:
        raise ValidationError("Valor requerido.")
    if value < min_value or value > max_value:
        raise ValidationError(f"El valor debe estar entre {min_value} y {max_value}.")


def validate_decimal_range(value: Decimal, min_value: Decimal, max_value: Decimal) -> None:
    if value is None:
        raise ValidationError("Valor requerido.")
    if value < min_value or value > max_value:
        raise ValidationError(f"El valor debe estar entre {min_value} y {max_value}.")


def validate_phone(value: str) -> None:
    if value and not PHONE_REGEX.match(value):
        raise ValidationError("Teléfono inválido. Use formato E.164 o 9-15 dígitos.")


def validate_max_length(value: str, max_length: int) -> None:
    if value is not None and len(value) > max_length:
        raise ValidationError(f"Longitud máxima permitida: {max_length}.")


def validate_choices(value: str, allowed: Iterable[str]) -> None:
    if value not in allowed:
        raise ValidationError("Valor fuera de los estados permitidos.")
