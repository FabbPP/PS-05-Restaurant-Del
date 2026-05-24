from decimal import Decimal

from apps.delivery.services import calculate_fee


def test_calculate_fee():
    assert calculate_fee(Decimal("1.00")) == Decimal("6.00")
