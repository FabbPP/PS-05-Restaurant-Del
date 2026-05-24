import pytest
from django.core.exceptions import ValidationError

from apps.core.enums import OrderType
from apps.orders.models import Order


def test_order_requires_table_for_dine_in():
    order = Order(order_type=OrderType.DINE_IN)
    with pytest.raises(ValidationError):
        order.full_clean()


def test_order_requires_customer_for_delivery():
    order = Order(order_type=OrderType.DELIVERY)
    with pytest.raises(ValidationError):
        order.full_clean()
