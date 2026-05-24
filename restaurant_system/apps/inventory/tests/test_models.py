import pytest
from django.core.exceptions import ValidationError

from apps.inventory.models import StockItem


def test_stock_negative_invalid(product):
    item = StockItem(product=product, quantity=-1, low_stock_threshold=1)
    with pytest.raises(ValidationError):
        item.full_clean()
