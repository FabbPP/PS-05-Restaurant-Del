import pytest
from django.core.exceptions import ValidationError

from apps.billing.models import Invoice


def test_invoice_negative_total_invalid(order_dine_in):
    invoice = Invoice(
        order=order_dine_in,
        document_type="RECEIPT",
        document_number="B001-1",
        total_amount=-1,
        payment_method="CASH",
    )
    with pytest.raises(ValidationError):
        invoice.full_clean()
