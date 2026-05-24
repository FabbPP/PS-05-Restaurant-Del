from decimal import Decimal

from apps.core.utils import quantize_money


def test_quantize_money():
    assert quantize_money(Decimal("10.005")) == Decimal("10.01")
