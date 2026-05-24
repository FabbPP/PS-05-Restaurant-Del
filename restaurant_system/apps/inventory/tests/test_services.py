import pytest

from apps.core.exceptions import StockError
from apps.inventory.services import adjust_stock


def test_adjust_stock_negative_not_allowed(stock_item):
    with pytest.raises(StockError):
        adjust_stock(item=stock_item, delta=-100, reason="test")
