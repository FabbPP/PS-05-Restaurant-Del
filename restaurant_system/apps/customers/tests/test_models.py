import pytest
from django.core.exceptions import ValidationError

from apps.customers.models import Customer


def test_customer_invalid_phone():
    customer = Customer(name="Test", email="test@example.com", phone="abc")
    with pytest.raises(ValidationError):
        customer.full_clean()
