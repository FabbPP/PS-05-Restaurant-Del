import pytest

from apps.core.enums import OrderStatus
from apps.core.exceptions import OrderStateError, StockError
from apps.orders.services import add_item, change_status


def test_add_item_requires_stock(order_dine_in, product):
    with pytest.raises(StockError):
        add_item(order=order_dine_in, product=product, quantity=1, unit_price=product.price)


def test_change_status_invalid(order_dine_in):
    with pytest.raises(OrderStateError):
        change_status(order=order_dine_in, new_status=OrderStatus.DELIVERED)
