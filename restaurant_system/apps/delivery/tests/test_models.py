import pytest
from django.core.exceptions import ValidationError

from apps.delivery.models import DeliveryInfo


def test_delivery_distance_invalid(order_delivery):
    info = DeliveryInfo(order=order_delivery, address="Av 1", phone="999888777", distance_km=20, estimated_time_min=10)
    with pytest.raises(ValidationError):
        info.full_clean()
