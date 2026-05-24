from __future__ import annotations

from decimal import Decimal

from apps.delivery.models import DeliveryInfo


BASE_FEE = Decimal("5.00")
PER_KM_FEE = Decimal("1.00")


def calculate_fee(distance_km: Decimal) -> Decimal:
    return BASE_FEE + (PER_KM_FEE * distance_km)


def estimate_time(distance_km: Decimal) -> int:
    # Critical: keep deterministic for tests and avoid external dependencies.
    return int(max(5, min(180, distance_km * Decimal("8"))))


def update_delivery_cost(info: DeliveryInfo) -> DeliveryInfo:
    info.delivery_fee = calculate_fee(info.distance_km)
    info.estimated_time_min = estimate_time(info.distance_km)
    info.save()
    return info
