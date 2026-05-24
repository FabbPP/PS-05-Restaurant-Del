import pytest
from django.core.exceptions import ValidationError

from apps.payments.models import Payment


def test_payment_amount_less_than_total(order_dine_in):
    order_dine_in.total = 10
    order_dine_in.save()
    payment = Payment(order=order_dine_in, method="CASH", amount=5)
    with pytest.raises(ValidationError):
        payment.full_clean()
