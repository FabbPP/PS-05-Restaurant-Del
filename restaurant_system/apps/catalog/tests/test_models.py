import pytest
from django.core.exceptions import ValidationError

from apps.catalog.models import Product


def test_product_price_invalid(category):
    product = Product(category=category, name="X", price="0.00")
    with pytest.raises(ValidationError):
        product.full_clean()
